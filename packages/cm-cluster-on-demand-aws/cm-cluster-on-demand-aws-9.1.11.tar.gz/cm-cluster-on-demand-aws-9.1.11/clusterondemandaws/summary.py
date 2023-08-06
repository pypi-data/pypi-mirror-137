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

from clusterondemand.summary import SummaryGenerator


class AwsSummaryGenerator(SummaryGenerator):
    """Generate the summary for creation of AWS clusters and nodes."""

    def __init__(self,
                 requested_clusters,
                 summary_type,
                 config,
                 head_node_definition,
                 head_image,
                 node_definition,
                 vpc_name,
                 vpc_id,
                 vpc_cidr_block,
                 subnet_texts):
        # Initialise the parent with an empty cluster name.
        # AWS supports the creation of multiple simultaneous clusters.
        # We use a different method for displaying the cluster names.
        super().__init__("", region=config["aws_region"], config=config, head_image=head_image,
                         primary_head_node_definition=head_node_definition, node_definitions=[node_definition],
                         summary_type=summary_type)
        self._requested_clusters = requested_clusters
        self._vpc_name = vpc_name
        self._vpc_id = vpc_id
        self._vpc_cidr = vpc_cidr_block
        self._subnet_texts = subnet_texts if subnet_texts else []

    def _add_rows(self, table):
        if self._config["existing_vpc_id"]:
            self._add_existing_vpc(table)

        self._add_head_node_ip_info(table)
        self._add_region(table)
        self._add_access_info(table)

    def _add_header(self, table):
        self._add_separator(table)
        self._add_cluster_names(table)
        self._add_separator(table)

    def _add_cluster_names(self, table):
        for cluster in self._requested_clusters:
            table.add_row(["Cluster:", cluster.name])

    def _add_existing_vpc(self, table):
        table.add_row(["Existing VPC:", f"{self._vpc_name} ({self._vpc_id}, {self._vpc_cidr})"])
        if not self._config["head_node_assign_public_ip"]:
            table.add_row(["", "Head node will NOT have a public IP assigned."])
        table.add_row(["", f"All subnets currently present in this VPC:"])
        for text in self._subnet_texts:
            table.add_row(["-", text])
        table.add_row(["", "(Subnets marked with '*' will get defined as Networks within the Bright cluster)"])
        self._add_separator(table)

    def _add_head_node_ip_info(self, table):
        if len(self._requested_clusters) == 1:
            head_ip = self._config["head_node_internal_ip"] if self._config["head_node_internal_ip"] \
                else "<auto> (set with --head-node-internal-ip)"
            table.add_row(["Head node IP: ", head_ip])
