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
import urllib.request
import xml.etree.ElementTree
from collections import defaultdict

import boto3
from botocore.exceptions import ClientError

from clusterondemand.exceptions import CODException, UserReportableException
from clusterondemandconfig import config

log = logging.getLogger("cluster-on-demand")


PRODUCTS_FILTER = [
    {"Type": "TERM_MATCH", "Field": "operatingSystem", "Value": "Linux"},
    {"Type": "TERM_MATCH", "Field": "preInstalledSw", "Value": "NA"},
    {"Type": "TERM_MATCH", "Field": "tenancy", "Value": "Shared"},
]

PRODUCT_FAMILIES = [
    {"Type": "TERM_MATCH", "Field": "productFamily", "Value": "Compute Instance"}
]


class NoTypesXMLError(Exception):
    """
    Raised when we failed to get the types XML file
    """
    def __init__(self, url):
        self.url = url


def list_regions():
    """Return a list of available regions in an AWS subscription."""
    aws_key_id = config["aws_access_key_id"]
    aws_secret = config["aws_secret_key"]
    region_name = config["aws_region"] or "eu-west-1"
    try:
        log.debug(f"Using '{region_name}' endpoint to list regions")
        ec2_client = boto3.client(
            "ec2", region_name=region_name,
            aws_access_key_id=aws_key_id,
            aws_secret_access_key=aws_secret
        )
        regions = ec2_client.describe_regions()["Regions"]
        region_names = [region["RegionName"] for region in regions]
        return region_names
    except ClientError as e:
        if "AWS was not able to validate the provided access credentials" in str(e):
            raise UserReportableException("The provided AWS credentials were invalid.")
        raise CODException("Error listing AWS regions", caused_by=e)


def make_long_to_short_region_map(region_short_names):
    """Return a dictionary with long names to short names, given a list of short names"""
    ssm_client = boto3.client("ssm", region_name="eu-west-1")

    def long_name(short_name):
        response = ssm_client.get_parameter(
            Name=f"/aws/service/global-infrastructure/regions/{short_name}/longName"
        )
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code != 200:
            raise Exception(f"Failed to find long name for region {short_name}")

        return response["Parameter"]["Value"]  # e.g: US West (N. California)

    long_to_short_map = {long_name(short_name): short_name for short_name in region_short_names}
    # A bit of a hack here...
    # Somehow, this ssm API returns for European regions "Europe (Frankfurt)"
    # While, the pricing api uses "EU (Frankfurt)". I don't know why, but to fix here
    # we add to the mapping both options and hope that they don't mean different regions in future
    long_to_short_map.update({
        long_name.replace("Europe ", "EU "): short_name
        for long_name, short_name in long_to_short_map.items()
        if long_name.startswith("Europe ")
    })

    return long_to_short_map


def fetch_available_instance_types_from_types_xml():
    """Return the available types, as specified in:
    https://support.brightcomputing.com/cloudroviders/amazon/types.xml"""
    region_to_types = defaultdict(set)

    try:
        contents = urllib.request.urlopen(config["types_url"]).read()
    except Exception as e:
        log.error(e)
        raise NoTypesXMLError(config["types_url"])
    root_node = xml.etree.ElementTree.fromstring(contents)
    for type_node in root_node.iter("type"):
        type_name = type_node.find("name").text
        for region_node in type_node.findall("ondemand"):
            region_name = region_node.find("region").text
            region_to_types[region_name].add(type_name)

    return region_to_types


def fetch_available_instance_types_from_aws():
    """Return a mapping of region to available instance types.
    Data comes from AWS pricing API, it might be slow"""
    all_regions = list_regions()
    log.info("Finding instance types for regions: %s", ", ".join(all_regions))
    long_to_short_regions = make_long_to_short_region_map(all_regions)

    region_to_types = defaultdict(set)
    pricing_api = boto3.client(
        "pricing",
        region_name="us-east-1",
        aws_access_key_id=config["aws_access_key_id"],
        aws_secret_access_key=config["aws_secret_key"],
    )
    for product_family in PRODUCT_FAMILIES:
        products_list = pricing_api.get_products(
            ServiceCode="AmazonEC2",
            Filters=[product_family] + PRODUCTS_FILTER,
        )

        if "NextToken" in products_list.keys():
            next_token = products_list["NextToken"]
        else:
            next_token = False
        while next_token:
            log.debug("Fetching instances type for product family: %s", product_family["Value"])
            for product in products_list["PriceList"]:
                product = json.loads(product)
                long_region = product["product"]["attributes"]["location"]
                if long_region not in long_to_short_regions:
                    continue
                region = long_to_short_regions[product["product"]["attributes"]["location"]]
                instance_type = product["product"]["attributes"]["instanceType"]
                region_to_types[region].add(instance_type)

            products_list = pricing_api.get_products(
                ServiceCode="AmazonEC2",
                Filters=[product_family] + PRODUCTS_FILTER,
                NextToken=next_token
            )
            if "NextToken" in products_list.keys():
                next_token = products_list["NextToken"]
            else:
                next_token = False
    return region_to_types


def get_available_instance_types():
    if config["fetch_from_aws"]:
        return fetch_available_instance_types_from_aws()
    else:
        return fetch_available_instance_types_from_types_xml()
