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

import logging
import shlex
import time
import yaml
from datetime import datetime
from typing import Dict, List

import six
import tenacity

from clusterondemand import utils
from clusterondemand.bcm_version import BcmVersion
from clusterondemand.clustercreate import enable_cmd_debug_commands
from clusterondemand.exceptions import CODException, UserReportableException
from clusterondemand.inbound_traffic_rule import InboundTrafficRule
from clusterondemandconfig import config

from .brightsetup import generate_bright_setup

log = logging.getLogger("cluster-on-demand")

BCM_TYPE_HEAD_NODE = "Head node"


def get_vpc_name_for_cluster(cluster_name):
    return config["fixed_cluster_prefix"] + cluster_name


def create_in_existing_vpc(cluster):
    """Create a cluster in a pre-existing (user-managed) VPC """

    ec2 = cluster.ec2
    vpc = ec2.Vpc(config["existing_vpc_id"])
    vpc.load()

    cluster.vpc = vpc

    # when using pre-existing VPC,   cluster_name != actual vpc name
    vpc.cluster_name = cluster.name

    if config["configure_igw_in_existing_vpc"]:
        assert config["i_know_configuring_igw_is_risky"]
        internet_gateway = _create_internet_gateway(cluster.vpc, ec2)
        _set_default_gateway_vpc(cluster.vpc, internet_gateway)
    else:
        log.info("Not configuring the Internet gateway in the VPC "
                 "(use --configure-igw-in-existing-vpc to change this).")

    # determine public subnet
    head_node_subnet_id = config["existing_subnet_id"][0]
    head_node_subnet = next(
        (subnet for subnet in vpc.subnets.all() if subnet.id == head_node_subnet_id),
        None)

    _report_progress(2, "Setting up VPC")

    if config["head_node_sg_id"] and config["node_sg_id"]:
        head_node_sg_id = config["head_node_sg_id"]
        node_sg_id = config["node_sg_id"]
    else:
        head_node_sg_id, node_sg_id = _create_security_groups(cluster.vpc, config["ingress_icmp"])

    head_node_hostname = cluster.name
    cluster.head_node = _create_head_node(
        cluster.vpc, head_node_hostname, head_node_subnet, cluster.head_node_image, head_node_sg_id, node_sg_id)

    _retry_not_found(_disable_source_dest_check, cluster.head_node)

    _report_progress(22, "Done setting up VPC for %s" % cluster.name)


def create_vpc(cluster):
    """Create an AWS VPC with the given name.

    This VPC contains a single head node, two subnets, an internal gateway and one routing table.
    """
    ec2 = cluster.ec2

    head_node_hostname = cluster.name
    vpc_name = get_vpc_name_for_cluster(cluster.name)

    if _vpc_with_name_exists(vpc_name, ec2):
        raise UserReportableException("VPC for this cluster already exists")

    _report_progress(2, "Setting up VPC")

    cluster.vpc = _create_vpc(cluster.name, vpc_name, ec2)
    cluster.vpc.name = vpc_name
    cluster.vpc.cluster_name = cluster.name

    if config["configure_igw"]:
        internet_gateway = _create_internet_gateway(cluster.vpc, ec2)
        _set_default_gateway_vpc(cluster.vpc, internet_gateway)
    else:
        log.debug("Not configuring the internet gateway in the VPC (set --configure-igw to change this)")

    public_subnet = _create_public_subnet(cluster.vpc, ec2)
    private_subnet = _create_private_subnet(cluster.vpc, ec2)

    if config["head_node_sg_id"] and config["node_sg_id"]:
        head_node_sg_id = config["head_node_sg_id"]
        node_sg_id = config["node_sg_id"]
    else:
        head_node_sg_id, node_sg_id = _create_security_groups(cluster.vpc, config["ingress_icmp"])

    cluster.head_node = _create_head_node(
        cluster.vpc, head_node_hostname, public_subnet, cluster.head_node_image, head_node_sg_id, node_sg_id)

    _retry_not_found(_disable_source_dest_check, cluster.head_node)

    log.info("Waiting for head node to be running")
    cluster.head_node.wait_until_running()  # must be running for being usable as gateway
    _set_default_gateway_subnet(cluster.vpc, private_subnet, cluster.head_node)

    _report_progress(22, "Done setting up VPC for %s" % vpc_name)


def _retry_not_found(func, *args, **kwargs):
    retry_wrapper = tenacity.Retrying(
        retry=tenacity.retry_if_exception_message(match=".*NotFound.*"),
        wait=tenacity.wait_exponential(multiplier=1, max=60),
        stop=tenacity.stop_after_delay(300),
        before_sleep=tenacity.before_sleep_log(log, logging.DEBUG),
        after=tenacity.after_log(log, logging.DEBUG),
        reraise=True,
    )
    return retry_wrapper(func, *args, **kwargs)


def _create_vpc(cluster_name, vpc_name, ec2):
    _report_progress(5, "Creating VPC for %s in %s..." % (vpc_name, config["aws_region"]))

    # https://aws.amazon.com/about-aws/whats-new/2020/07/amazon-vpc-resources-support-tag-on-create/
    tags = _construct_bright_tags(cluster_name, vpc_name)
    kwargs = {"CidrBlock": str(config["vpc_cidr"]),
              "TagSpecifications": [{"ResourceType": "vpc", "Tags": tags}]}

    vpc = ec2.create_vpc(**kwargs)
    # Make sure the VPC has finished creation before using it.
    vpc.wait_until_exists()
    _retry_not_found(vpc.wait_until_available)
    log.debug("VPC was successfully created, id: %s", vpc.id)

    return vpc


def _create_internet_gateway(vpc, ec2):
    _report_progress(10, "Adding internet connectivity...")

    internet_gateway_name = vpc.cluster_name
    tags = _construct_bright_tags(vpc.cluster_name, internet_gateway_name)
    kwargs = {"TagSpecifications": [{"ResourceType": "internet-gateway", "Tags": tags}]}

    internet_gateway = ec2.create_internet_gateway(**kwargs)
    time.sleep(0.5)

    internet_gateway.name = internet_gateway_name

    vpc.attach_internet_gateway(InternetGatewayId=internet_gateway.id)
    return internet_gateway


def _create_public_subnet(vpc, ec2):
    _report_progress(12, "Creating public subnet...")
    kwargs = {"CidrBlock": str(config["public_subnet_cidr"])}

    if config["aws_availability_zone"]:
        kwargs["AvailabilityZone"] = config["aws_availability_zone"]

    public_subnet_name = vpc.cluster_name + " public"
    tags = _construct_bright_tags(vpc.cluster_name, public_subnet_name, BCM_TYPE_HEAD_NODE)
    kwargs["TagSpecifications"] = [{"ResourceType": "subnet", "Tags": tags}]

    public_subnet = vpc.create_subnet(**kwargs)
    time.sleep(0.5)
    public_subnet.name = public_subnet_name

    return public_subnet


def _create_private_subnet(vpc, ec2):
    _report_progress(14, "Creating private subnet...")

    kwargs = {"CidrBlock": str(config["private_subnet_cidr"])}

    if config["aws_availability_zone"]:
        kwargs["AvailabilityZone"] = config["aws_availability_zone"]

    private_subnet_name = vpc.cluster_name + " private"
    tags = _construct_bright_tags(vpc.cluster_name, private_subnet_name, BCM_TYPE_HEAD_NODE)
    kwargs["TagSpecifications"] = [{"ResourceType": "subnet", "Tags": tags}]

    private_subnet = vpc.create_subnet(**kwargs)
    time.sleep(0.5)
    private_subnet.name = private_subnet_name

    return private_subnet


def _set_default_gateway_vpc(vpc, internet_gateway):
    main_route_table = _find_main_route_table(vpc)
    main_route_table.create_route(DestinationCidrBlock="0.0.0.0/0", GatewayId=internet_gateway.id)


# When the default gateway of the subnet is an ec2 instance the ec2 instance must be in
# the running state. Even though we make sure to check that an instance is running before
# we set the gateway, we can still encounter incorrect instance state errors.
@tenacity.retry(
    retry=tenacity.retry_if_exception_message(match=".*IncorrectInstanceState.*"),
    wait=tenacity.wait_exponential(multiplier=1, max=60),
    stop=tenacity.stop_after_delay(300),
    before_sleep=tenacity.before_sleep_log(log, logging.DEBUG),
    after=tenacity.after_log(log, logging.DEBUG),
    reraise=True
)
def _set_default_gateway_subnet(vpc, subnet, internet_gateway):
    route_table_name = subnet.name + " route table"
    tags = _construct_bright_tags(vpc.cluster_name, route_table_name)
    rt_kwargs = {"TagSpecifications": [{"ResourceType": "route-table", "Tags": tags}]}

    route_table = vpc.create_route_table(**rt_kwargs)

    route_table.name = route_table_name

    route_table.associate_with_subnet(SubnetId=subnet.id)

    kwargs = {"DestinationCidrBlock": "0.0.0.0/0"}
    if "ec2.Instance" == internet_gateway.__class__.__name__:
        kwargs["InstanceId"] = internet_gateway.id
    route_table.create_route(**kwargs)


def _create_head_node(vpc, hostname, public_subnet, head_node_image, head_node_sg_id, node_sg_id):
    _report_progress(16, "Creating head node (%s)..." % config["head_node_type"])
    bdm = None
    if config["head_node_root_volume_size"]:
        bdm = [
            {
                "DeviceName": "/dev/sda1",
                "Ebs": {
                    "VolumeSize": config["head_node_root_volume_size"],
                    "VolumeType": config["head_node_root_volume_type"],
                    "DeleteOnTermination": True
                }
            }
        ]
        if config["head_node_root_volume_type"] in ["io1", "io2"]:
            bdm[0]["Ebs"]["Iops"] = config["head_node_root_volume_iops"]

    bright_setup = generate_bright_setup(
        hostname=hostname,
        head_node_sg_id=head_node_sg_id,
        node_sg_id=node_sg_id,
        existing_subnet_ids=config["existing_subnet_id"] if config["existing_subnet_id"] else None)

    cloud_init_script = """#!/bin/sh
        echo '%s' > /root/cm/cm-bright-setup.conf
    """ % yaml.dump(bright_setup, default_flow_style=False).replace("'", '"')

    cloud_init_script += """
        echo "%s" > /root/cm/node-disk-setup.xml
    """ % config["node_disk_setup"]

    # The code below the code that is getting patched here still support only 1 or 2 subnets. And that's fine.
    # At this point we simply want to enable creating a cluster in a env with more than 2 subnets (while allowing the
    # user to specify only 1 or 2 of those).
    if config["existing_subnet_id"]:
        # if  "config["existing_subnet_id"]" is not set, we must not patch.
        cloud_init_script += \
            "sed -i 's/subnets = list(self.head_node_instance.vpc.subnets.all())/" \
            "subnets = [subnet for subnet in list(self.head_node_instance.vpc.subnets.all()) " \
            "if subnet.id in self.config[\"amazon\"][\"existing_subnet_ids\"]]/g' " \
            "/cm/local/apps/cm-setup/lib/python3.7/site-packages/cmsetup/plugins/brightsetup/stages.py\n"
        # This code also has a check
        # if len(subnets) > 2:
        #    raise Exception('VPCs with more than one subnets are not supported')
        # we don't need to remove it, as with the patch above, the num of subnets there will be limited to
        # the subnets specified with --existing-subnet-id,  which on the clientside will ensure this is 1 or 2,

    kwargs = {
        "ImageId": head_node_image.uuid,
        "MinCount": 1,
        "MaxCount": 1,
        "InstanceType": config["head_node_type"],
        "BlockDeviceMappings": bdm,
    }
    if config["head_node_internal_ip"]:
        kwargs["PrivateIpAddress"] = config["head_node_internal_ip"]

    if config["ssh_key_pair"]:
        log.info("Key pair specified")
        kwargs["KeyName"] = config["ssh_key_pair"]
    if config["ssh_pub_key_path"]:
        log.info("Public key specified")
        with open(config["ssh_pub_key_path"]) as pub_key:
            cloud_init_script += """
            mkdir -p /root/.ssh/
            echo '# COD injected public key' >> /root/.ssh/authorized_keys
            echo '%s' >> /root/.ssh/authorized_keys
            """ % pub_key.read()

    cloud_init_script += """
        echo %s | chpasswd
    """ % shlex.quote("root:" + config["cluster_password"])

    if config["ssh_password_authentication"]:
        cloud_init_script += """
        sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
        if ! systemctl try-reload-or-restart sshd; then
          echo 'Old systemd, using different reload command.'
          systemctl reload-or-try-restart sshd
        fi
        """
        log.info("Enabling ssh password authentication")

    if config["cmd_debug"]:
        subsystems = config["cmd_debug_subsystems"]
        log.debug(f"Setting debug mode on CMDaemon for subsystems: '{subsystems}'")
        for command in enable_cmd_debug_commands(subsystems):
            cloud_init_script += command + "\n"

    if config["run_cm_bright_setup"]:
        if config["prebs"]:
            cloud_init_script += "\n".join(["echo 'Starting custom prebs commands'", *config["prebs"], ""])

        if BcmVersion(config["version"]) < "8.2":
            cloud_init_script += "/cm/local/apps/cluster-tools/bin/cm-bright-setup " \
                                 "-c /root/cm/cm-bright-setup.conf --on-error-action abort\n"
        else:
            cloud_init_script += "/cm/local/apps/cm-setup/bin/cm-bright-setup " \
                                 "-c /root/cm/cm-bright-setup.conf --on-error-action abort\n"

        if config["postbs"]:
            cloud_init_script += "\n".join(["echo 'Starting custom postbs commands'", *config["postbs"], ""])
    else:
        log.info("Not Running cm-bright-setup")

    if config["head_node_pg_name"]:
        kwargs["Placement"] = {"GroupName": config["head_node_pg_name"]}

    kwargs["UserData"] = cloud_init_script

    kwargs["SecurityGroupIds"] = [head_node_sg_id]

    log.info("Creating the head node VM instance")

    head_node_instance_name = f"{vpc.cluster_name} (Bright COD-AWS {config['version']} head node)"
    tags = _construct_bright_tags(vpc.cluster_name, head_node_instance_name, BCM_TYPE_HEAD_NODE)
    kwargs["TagSpecifications"] = [{"ResourceType": "instance", "Tags": tags}]

    instances = public_subnet.create_instances(**kwargs)
    head_node_instance = instances[0]
    log.info(f"Created VM {head_node_instance.id}")

    log.debug("Waiting for VM to exist so that we can assign tags")
    _retry_not_found(head_node_instance.wait_until_exists)

    log.debug("Applying tags to the head node VM instance")
    return head_node_instance


def _create_security_groups(vpc, ingress_icmp_cidr):
    head_sg = vpc.create_security_group(
        GroupName=f"Bright {vpc.cluster_name}-headnode",
        Description=f"Security group for head node in Bright COD-AWS cluster {vpc.cluster_name}"
    )
    log.info(f"Created security group for the head node: {head_sg.id}")

    node_sg = vpc.create_security_group(
        GroupName=f"Bright {vpc.cluster_name}-node",
        Description=f"Security group for compute nodes in Bright COD-AWS cluster {vpc.cluster_name}"
    )
    log.info(f"Created security group for the compute node: {node_sg.id}")

    log.debug("Configuring the security groups")
    # Configure head node sec group
    for inbound_rule in InboundTrafficRule.process_inbound_rules(config["inbound_rule"]):
        head_sg.authorize_ingress(
            IpProtocol=inbound_rule.protocol,
            FromPort=int(inbound_rule.dst_first_port),
            ToPort=int(inbound_rule.dst_last_port),
            CidrIp=inbound_rule.src_cidr,
        )

    # Enable node to head access
    head_sg.authorize_ingress(
        IpPermissions=[{"IpProtocol": "-1", "UserIdGroupPairs": [{"GroupId": node_sg.id}]}]
    )

    # Allow incoming ICMP to head
    if ingress_icmp_cidr:
        head_sg.authorize_ingress(
            IpProtocol="icmp",
            FromPort=-1,
            ToPort=-1,
            CidrIp=str(ingress_icmp_cidr),
        )

    # Allow for node to node, and head to node.
    node_sg.authorize_ingress(
        IpPermissions=[
            {
                "IpProtocol": "-1",
                "UserIdGroupPairs": [
                    {"GroupId": head_sg.id},
                    {"GroupId": node_sg.id},
                ],
            }
        ]
    )
    return head_sg.id, node_sg.id


def _disable_source_dest_check(head_node_instance):
    head_node_instance.modify_attribute(SourceDestCheck={"Value": False})


def _report_progress(percentage, action):
    utils.cod_log(log, action, percentage)


def _vpc_with_name_exists(vpc_name, ec2):
    vpcs = list(ec2.vpcs.filter(Filters=[{
        "Name": "tag:Name",
        "Values": [vpc_name]
    }]))

    return True if vpcs else False


def _find_main_route_table(vpc):
    route_tables = list(vpc.route_tables.filter(
        Filters=[{
            "Name": "association.main",
            "Values": ["true"]
        }]
    ))
    assert 1 == len(route_tables)
    return route_tables[0]


def _construct_bright_tags(cluster_name, obj_name, bcm_type=None):
    tags = {
        "BCM Created at": datetime.utcnow().isoformat() + "Z",  # fix missing timezone
        "BCM Created by": utils.get_user_at_fqdn_hostname(),
        "BCM Cluster": cluster_name,
        "BCM Bursting": "on-demand",
        # This one has to follow a slightly different naming convention (i.e. no "BCM"
        # prefix), because this tag has a special meaning for AWS.
        "Name": obj_name
    }
    if bcm_type:
        tags["BCM Type"] = bcm_type

    tags.update(dict((str(k), str(v)) for k, v in config["cluster_tags"]))
    tags = [{"Key": key, "Value": value} for key, value in six.iteritems(tags)]
    return tags


def get_aws_tag(tags: List[Dict[str, str]], name: str, default: str = None) -> str:
    """
    For some mysterious reason, boto3 stores tags as a list of dictionaries:
    [{'Key': 'Name', 'Value': 'my-value-foo'}].
    This function retrieves the value
    """

    if tags is not None:
        for tag in tags:
            if tag["Key"] == name:
                return tag["Value"]

    if default is not None:
        return default
    else:
        raise CODException(f"The AWS tag '{name}' was not found within {len(tags)} tags.")
