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

import clusterondemand.brightsetup
from clusterondemand.bcm_version import BcmVersion
from clusterondemand.configuration import NO_WLM
from clusterondemandconfig import config


def generate_bright_setup(hostname, head_node_sg_id, node_sg_id, existing_subnet_ids):
    license_dict = clusterondemand.brightsetup.get_license_dict(hostname)
    brightsetup = clusterondemand.brightsetup.generate_bright_setup(
        cloud_type="aws",
        wlm=config["wlm"] if config["wlm"] != NO_WLM else "",
        hostname=hostname,
        password=config["cluster_password"],
        node_count=config["nodes"],
        timezone=config["timezone"],
        license_dict=license_dict,
        node_kernel_modules=["nvme", "ena"],
        node_disk_setup_path="/root/cm/node-disk-setup.xml"
    )

    brightsetup["modules"]["brightsetup"]["amazon"] = {
        # WARN CM-34877: In versions before 9.0 this field was unused. For 9.0 and 9.1 we repurposed it
        # in order to change the default region to list other regions
        "username": config["aws_region"],
        "nodes": {
            "count": config["nodes"],
            "storage": {
                "type": "EBS",
                "size": 42,
            },
            "base_name": "cnode",
            "type": config["node_type"],
        },
        "extra_disks": [],
        "account_id": config["aws_account_id"],
        "access_key": config["aws_access_key_id"],
        "secret_key": config["aws_secret_key"],
        "head_node_security_group_id": head_node_sg_id,
        "nodes_security_group_id": node_sg_id,
    }

    # Series of customizations depending on version
    # TODO CM-35193: We have to actually check for the revision, because these changes below work on
    #                9.0-dev and 9.1-dev, but not on older versions. To do that properly, we need also
    #                the changes from CM-35092
    if BcmVersion(config["version"]) == "9.1":
        brightsetup["modules"]["brightsetup"]["amazon"]["image_owners"] = [config["image_owner"]]
        # CM-34877: In version 9.1 the username field was unused, so we repurposed it to get the API region
        brightsetup["modules"]["brightsetup"]["amazon"]["username"] = config["aws_region"]
    elif BcmVersion(config["version"]) == "9.0":
        # CM-34877: In version 9.0 the username field was unused, so we repurposed it to get the API region
        brightsetup["modules"]["brightsetup"]["amazon"]["username"] = config["aws_region"]

    if existing_subnet_ids:
        brightsetup["modules"]["brightsetup"]["amazon"]["existing_subnet_ids"] = existing_subnet_ids

    return brightsetup
