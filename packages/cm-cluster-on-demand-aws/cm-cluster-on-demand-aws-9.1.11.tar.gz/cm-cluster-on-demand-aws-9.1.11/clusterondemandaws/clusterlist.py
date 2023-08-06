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

from __future__ import absolute_import, print_function

import logging

import clusterondemand.configuration
from clusterondemand.codoutput.sortingutils import SortableData
from clusterondemandaws.base import ClusterCommandBase
from clusterondemandconfig import ConfigNamespace, config

from .cluster import Cluster
from .configuration import awscommon_ns
from .ec2connection import establish_connection_to_ec2

log = logging.getLogger("cluster-on-demand")

ALL_COLUMNS = [
    ("cluster_name", "Cluster Name"),
    ("vpc_id", "VPC ID"),
    ("Head node ID", "Head node ID"),
    ("public_ip", "Public IP"),
    ("state", "State"),
    ("type", "Type"),
    ("image_name", "Image Name"),
    ("created", "Image Created"),
]


def run_command():
    return ClusterList().run()


config_ns = ConfigNamespace("aws.cluster.list", "list output parameters")
config_ns.import_namespace(awscommon_ns)
config_ns.import_namespace(clusterondemand.configuration.clusterlist_ns)
config_ns.add_enumeration_parameter(
    "sort",
    default=["created"],
    choices=[column[0] for column in ALL_COLUMNS],
    help="Sort results by one (or two) of the columns"
)
config_ns.add_enumeration_parameter(
    "columns",
    choices=[column[0] for column in ALL_COLUMNS],
    help="Provide space separated set of columns to be displayed"
)
config_ns.add_repeating_positional_parameter(
    "filters",
    default=["*"],
    require_value=True,
    help="Cluster names or patterns to be listed. Default: all clusters. Wildcards are supported (e.g: prefix-*)",
)


class ClusterList(ClusterCommandBase):

    def _validate_params(self):
        self._validate_aws_access_credentials()

    def run(self):
        self._validate_params()

        ec2, ec2c = establish_connection_to_ec2()
        log.info("Listing clusters in region %s" % config["aws_region"])

        clusters = list(Cluster.find(ec2, ec2c, config["filters"]))
        if clusters:
            rows = []
            for cluster in clusters:
                head_node = cluster.head_node

                row = []
                row += [cluster.name]
                row += [cluster.vpc.id]
                row += [cluster.head_node.id if cluster.head_node else "missing"]
                row += [cluster.head_node.public_ip_address
                        if cluster.head_node and cluster.head_node.public_ip_address else ""]
                row += [cluster.head_node.state["Name"] if cluster.head_node else ""]
                row += [cluster.head_node.instance_type if cluster.head_node else ""]

                if head_node and head_node.image_id:
                    img = ec2.Image(cluster.head_node.image_id)
                else:
                    img = None
                row += [_safe_image_name(img) if img else "none"]
                row += [_safe_image_creation_date(img) if img else "none"]

                rows.append(row)

            cols_id = config["columns"]
            if not cols_id:
                cols_id = [column[0] for column in ALL_COLUMNS]
            table = SortableData(all_headers=ALL_COLUMNS, requested_headers=cols_id, rows=rows)
            table.sort(*config["sort"])

            print(table.output(output_format=config["output_format"]))

        else:
            log.info("No clusters found.")


def _safe_image_name(img):
    try:
        return img.name
    except AttributeError:
        return "<unknown>"


def _safe_image_creation_date(img):
    try:
        return img.creation_date
    except AttributeError:
        return "<unknown>"
