# Copyright 2004-2022 Bright Computing Holding BV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import collections
import logging
import time

from clusterondemand.exceptions import CODException, UserReportableException
from clusterondemandconfig import config

from .vpc import BCM_TYPE_HEAD_NODE

log = logging.getLogger("cluster-on-demand")


class Cluster(object):
    # AWS eIP assignment failures occur rarely and can be worked around
    # by retrying for 2.5+ minutes (see CM-9991).
    # Let's make it 5 minutes to make sure we don't leave an eIP allocation unassigned,
    # which costs money.
    IP_ASSIGNMENT_RETRY_DELAY = 10
    IP_ASSIGNMENT_RETRIES = 30

    def __init__(self, ec2, ec2c, name, head_node_image=None, vpc=None, head_node=None):
        self.ec2 = ec2
        self.ec2c = ec2c
        self.name = name
        self.vpc = vpc
        self.head_node_image = head_node_image
        self.head_node = head_node or self.find_head_node()
        self.error_message = None

    @classmethod
    def get_vpc_name(cls, vpc):
        for tag in vpc.tags:
            if tag["Key"] == "Name":
                return tag["Value"]

        raise CODException("No Name tag found")

    @classmethod
    def find(cls, ec2, ec2c, names):
        patterns = [f"{config['fixed_cluster_prefix']}{name}" for name in names]
        log.debug("Searching for vpcs with tag:name %s" % patterns)
        for vpc in ec2.vpcs.filter(
                Filters=[{"Name": "tag:Name",
                          "Values": patterns}]):
            vpc_name = cls.get_vpc_name(vpc)
            cluster_name = vpc_name[len(config["fixed_cluster_prefix"]):]
            yield cls(ec2, ec2c, cluster_name, vpc=vpc)

    def __unicode__(self):
        return "{} {!r} {!r} {}".format(self.name,
                                        self.vpc,
                                        self.head_node,
                                        self.head_node and self.head_node.state["Name"])

    def find_head_node(self):
        if not self.vpc:
            return None

        instances = list(self.vpc.instances.filter(Filters=[
            {"Name": "tag:BCM Type", "Values": [BCM_TYPE_HEAD_NODE]},
            {"Name": "instance-state-name",
             "Values": ["pending", "running", "shutting-down", "stopping", "stopped"]},
        ]))

        if not instances:
            return None

        if len(instances) == 1:
            return instances[0]

        raise CODException("More than one head node found for cluster %s (%r)" % (self.name, self.vpc))

    def assign_eip(self):
        # Find public net interface
        for network_interface in self.head_node.network_interfaces:
            network_interface.reload()
            if network_interface.attachment["DeviceIndex"] == 0:
                # If Elastic IP already assign, do nothing
                if network_interface.association:
                    return
                public_network_interface_id = network_interface.id
                break
        else:
            raise CODException("Could not find public_network_interface_id")

        # Public IP
        allocation_id = self.ec2c.allocate_address(Domain="vpc")["AllocationId"]
        vpc_address = self.ec2.VpcAddress(allocation_id)
        retries = self.IP_ASSIGNMENT_RETRIES
        while True:
            try:
                vpc_address.associate(NetworkInterfaceId=public_network_interface_id)
            except Exception as e:
                if retries == 0:
                    try:
                        vpc_address.release()
                    except Exception:
                        pass  # suppress errors in release() which would mask the original error
                    raise CODException("Error assigning IP", caused_by=e)
                else:
                    log.info(f"Retrying attempt to assign IP in {self.IP_ASSIGNMENT_RETRY_DELAY} seconds... "
                             f"({retries} retries left, reason: {str(e)}")
                    time.sleep(self.IP_ASSIGNMENT_RETRY_DELAY)
                    retries -= 1
            else:
                break

        # Refresh public_ip_address on head node
        self.head_node.reload()
        log.info(f"Elastic IP assigned: {self.head_node.public_ip_address}")

    def release_eip(self):
        if self.head_node:
            self.head_node.reload()
            for network_interface in self.head_node.network_interfaces:
                # I think without it association is often? empty
                network_interface.reload()
                # We only assign eip to first device
                if network_interface.attachment["DeviceIndex"] == 0:
                    if network_interface.association:
                        vpc_address = network_interface.association.address
                        network_interface.association.delete()
                        vpc_address.release()

    @classmethod
    def destroy(cls, clusters):
        # Only destroy those for which vpc was actually created
        vpcs = [cluster.vpc for cluster in clusters if cluster.vpc]

        for cluster in clusters:
            cluster.release_eip()

        cls.destroy_vpcs(vpcs)

        for cluster in clusters:
            cluster.vpc = None
            cluster.head_node = None

    @classmethod
    def destroy_vpcs(cls, vpcs):
        log.info("Stopping instances for VPCs %s", " ".join(cls.get_vpc_name(vpc) for vpc in vpcs))

        log.info("Listing instances...")
        instances = [
            instance
            for vpc in vpcs
            for instance in vpc.instances.all()
        ]

        # We want to terminate all instances here and wait until they are terminated.
        # That should be faster than
        # request termination and wait sequentially in destroy_vpc methods
        log.info("Issuing instances termination requests...")
        for instance in instances:
            instance.terminate()

        log.info("Waiting until instances terminated...")
        for instance in instances:
            instance.wait_until_terminated()

        for vpc in vpcs:
            cls.destroy_vpc(vpc)

    @classmethod
    def destroy_vpc(cls, vpc):
        vpc_name = cls.get_vpc_name(vpc)
        log.info("Destroying VPC %s", vpc_name)

        log.info("Deleting subnets...")
        for subnet in vpc.subnets.all():
            subnet.delete()

        log.info("Deleting route tables...")
        for route_table in vpc.route_tables.all():
            if not cls._is_main_routing_table(route_table):
                route_table.delete()

        log.info("Detaching and deleting gateways...")
        for gateway in vpc.internet_gateways.all():
            vpc.detach_internet_gateway(InternetGatewayId=gateway.id)
            gateway.delete()

        # Flush all permissions, because if they refer to security group,
        # that security group won't be deleted
        log.info("Flushing permissions...")
        for sg in vpc.security_groups.all():
            if sg.ip_permissions:
                sg.revoke_ingress(IpPermissions=sg.ip_permissions)
            if sg.ip_permissions_egress:
                sg.revoke_egress(IpPermissions=sg.ip_permissions_egress)

        # Delete security groups themselves
        log.info("Deleting security groups...")
        for sg in vpc.security_groups.all():
            if sg.group_name != "default":
                sg.delete()

        log.info("Deleting VPC...")
        vpc.delete()

        log.info("Done destroying VPC %s", vpc_name)

    @classmethod
    def stop(cls, clusters, release_eip):
        if release_eip:
            for cluster in clusters:
                cluster.release_eip()

        instances = [
            instance for cluster in clusters for instance in cluster.vpc.instances.all()
        ]

        log.info("Issuing stop request...")
        for instance in instances:
            instance.stop()

        log.info("Waiting until stopped...")
        for instance in instances:
            instance.wait_until_stopped()

    @classmethod
    def start(cls, clusters):
        head_nodes = [c.head_node for c in clusters]

        log.info("Issuing start requests...")
        for head_node in head_nodes:
            head_node.start()

        log.info("Wait until started...")
        for head_node in head_nodes:
            head_node.wait_until_running()

        for cluster in clusters:
            cluster.assign_eip()

    @classmethod
    def find_some(cls, ec2, ec2c, prefix=None, names=None):
        if names:
            log.debug("Checking for name")
            # Check for duplicate names
            cnt = collections.Counter(names)
            duplicate_names = [name for name, count in cnt.items() if count > 1]
            if duplicate_names:
                raise UserReportableException(
                    "Duplicate cluster names: %s" % " ".join(duplicate_names))

            # Add prefix if present
            if prefix:
                names = ["%s-%s" % (prefix, name) for name in names]

            # Check if specified cluster exists
            all_clusters = list(Cluster.find(ec2, ec2c, names))
            all_cluster_names = [c.name for c in all_clusters]
            log.debug("Checking for matches in %s" % all_cluster_names)
            clusters = [
                cluster for cluster in all_clusters
                if cluster.name in names
            ]
            found_names = {cluster.name for cluster in clusters}

            # Use filtering instead of set operation here, to keep names order specified by user
            not_found_names = [name for name in names if name not in found_names]
            if not_found_names:
                raise CODException("Clusters not found: %s" % " ".join(not_found_names))

            return clusters
        elif prefix:
            log.debug("Checking for prefix %s" % prefix)
            return list(Cluster.find(ec2, ec2c, [prefix + "*"]))

        raise CODException("If you don't specify prefix, you need to specify cluster names")

    @classmethod
    def _is_main_routing_table(cls, route_table):
        for association in route_table.associations_attribute:
            if association.get("Main"):
                return True
        return False
