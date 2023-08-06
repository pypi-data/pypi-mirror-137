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

from clusterondemand.clusternameprefix import clusterprefix_ns, ensure_cod_prefix
from clusterondemand.exceptions import CODException
from clusterondemand.utils import confirm, confirm_ns
from clusterondemandaws.base import ClusterCommandBase
from clusterondemandconfig import ConfigNamespace, config

from .cluster import Cluster
from .configuration import awscommon_ns
from .ec2connection import establish_connection_to_ec2

log = logging.getLogger("cluster-on-demand")


def run_command():
    return ClusterDelete().run()


config_ns = ConfigNamespace("aws.cluster.delete", "cluster delete parameters")
config_ns.import_namespace(awscommon_ns)
config_ns.import_namespace(clusterprefix_ns)
config_ns.import_namespace(confirm_ns)
config_ns.add_repeating_positional_parameter(
    "name",
    help="Name(s) of the cluster to remove"
)
config_ns.add_parameter(
    "prefix",
    env="COD_AWS_PREFIX",  # TODO (CM-26949): Get rid of this parameter and use the cod_prefix
    help="Prefix of clusters to be removed")


class ClusterDelete(ClusterCommandBase):

    def _validate_params(self):
        if config["name"]:
            self._validate_cluster_names()
        self._validate_aws_access_credentials()

    def run(self):
        self._validate_params()

        ec2, ec2c = establish_connection_to_ec2()
        prefix = None
        names = [ensure_cod_prefix(name) for name in config["name"]]
        if not names:
            prefix = config["prefix"]

        clusters = Cluster.find_some(ec2, ec2c, prefix, names)
        if clusters:
            names = [cluster.name for cluster in clusters]

            log.info("This will destroy VPCs for %s, continue?" % (" ".join(names),))
            if not confirm():
                return

            Cluster.destroy(clusters)

        else:
            raise CODException("No clusters found")
