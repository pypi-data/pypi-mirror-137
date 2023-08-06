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

import json
import logging

import six
import six.moves.urllib.error
import six.moves.urllib.parse
import six.moves.urllib.request

import clusterondemand.configuration
from clusterondemand.codoutput.sortingutils import SortableData
from clusterondemand.exceptions import CODException, UserReportableException
from clusterondemandconfig import ConfigNamespace, config

from .configuration import awscommon_ns, awsinstancetype_ns
from .instancetype import NoTypesXMLError, get_available_instance_types, list_regions

columns = [
    ("region", "Region"),
    ("instancetype", "Instance Type")
]
log = logging.getLogger("cluster-on-demand")


HR = "---------------------------------------------------------------------"
TYPES_URL = "http://support.brightcomputing.com/cloudproviders/amazon/types.xml"


config_ns = ConfigNamespace("aws.instancetype.list", "list output parameters")
config_ns.import_namespace(awscommon_ns)
config_ns.import_namespace(awsinstancetype_ns)
config_ns.import_namespace(clusterondemand.configuration.clusterlist_ns)
config_ns.add_enumeration_parameter(
    "sort",
    default=["region"],
    choices=[col[0] for col in columns],
    help="Column according to which the table should be sorted (asc order)."
)
config_ns.add_parameter(
    "region",
    help="Only show instance types for this region."
)
config_ns.override_imported_parameter(
    "output_format",
    choices=["table", "json"],
    help_varname=None,
)

PRODUCTS_FILTER = [
    {"Type": "TERM_MATCH", "Field": "operatingSystem", "Value": "Linux"},
    {"Type": "TERM_MATCH", "Field": "preInstalledSw", "Value": "NA"},
    {"Type": "TERM_MATCH", "Field": "tenancy", "Value": "Shared"},
]

PRODUCT_FAMILIES = [
    {"Type": "TERM_MATCH", "Field": "productFamily", "Value": "Compute Instance"}
]


def run_command():
    return InstanceTypesList().run()


class InstanceTypesList(object):
    @classmethod
    def map_regions_to_instance_types(cls, chosen_region=None):
        regions = [chosen_region] if chosen_region else list_regions()
        instance_types = get_available_instance_types()
        mapping = {region: types for region, types in six.iteritems(instance_types)
                   if region in regions}
        return mapping

    def output_json_file(self):
        """Print out all mappings in JSON format."""
        # self.mapping is a map {str: set}, because we don't want duplicates, but json.dumps cannot understand it
        # Let's convert to a list. And sort it so the output is always the same
        sorted_map = {"regions": {key: sorted(list(value)) for key, value in self.mapping.items()}}

        region_to_instance_types_json = json.dumps(sorted_map, indent=4, sort_keys=True)
        print(region_to_instance_types_json)

    def output_prettytable(self, all_columns):
        """Print all mappings in a Table."""
        region_to_instancetype = []
        for key, value in six.iteritems(self.mapping):
            for val in value:
                region_to_instancetype.append([
                    key,
                    val
                ])
        cols_id = [column[0] for column in all_columns]
        table = SortableData(
            all_headers=all_columns,
            requested_headers=cols_id,
            rows=region_to_instancetype
        )
        table.sort(*config["sort"])
        print(table.output(output_format=config["output_format"]))

    def run(self):
        region = config["region"]

        all_regions = list_regions()
        if region and region not in all_regions:
            available_regions = ", ".join(all_regions)
            raise CODException(
                "Region '{region}' is not a valid AWS region or is not available for this subscription. "
                "Available regions are: {available_regions}".format(
                    region=region,
                    available_regions=available_regions
                )
            )

        try:
            self.mapping = self.map_regions_to_instance_types(region)
        except NoTypesXMLError as e:
            raise UserReportableException(
                f"Failed to read instance types file from '{e.url}'. You can use --types-url to set a different URL or "
                f"use --fetch-from-aws to use the (slower) AWS pricing API directly."
            )

        if config["output_format"] == "json":
            self.output_json_file()
        elif config["output_format"] == "table":
            self.output_prettytable(columns)
