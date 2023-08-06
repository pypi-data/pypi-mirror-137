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

import re

import boto3

from .instancetype import get_available_instance_types, list_regions

ACCOUNT_ID_REGEX = r"^[0-9]{12}$"
ACCESS_KEY_ID_REGEX = r"^[0-9A-Z]{16,128}$"


def list_availability_zones(region, aws_key_id, aws_secret):
    """Return a list of availabilityzones in an AWS subscription."""
    ec2_client = boto3.client(
        "ec2", region_name=region,
        aws_access_key_id=aws_key_id,
        aws_secret_access_key=aws_secret
    )
    azs = ec2_client.describe_availability_zones()
    az_names = [az["ZoneName"] for az in azs["AvailabilityZones"]]
    return az_names


class AWSParamValidator(object):
    valid_instance_types = None  # cache to avoid repeated fetches

    @staticmethod
    def validate_availability_zone(availability_zone, region, aws_key_id, aws_secret):
        return availability_zone in list_availability_zones(
            region, aws_key_id, aws_secret
        )

    @staticmethod
    def validate_region(region, aws_key_id, aws_secret):
        return region in list_regions()

    @classmethod
    def validate_instance_type(cls, region, instance_type):
        if cls.valid_instance_types is None:
            cls.valid_instance_types = get_available_instance_types()

        return instance_type in cls.valid_instance_types[region]

    @staticmethod
    def validate_access_key_id_format(access_key_id):
        return isinstance(access_key_id, str) and bool(re.match(ACCESS_KEY_ID_REGEX, access_key_id))

    @staticmethod
    def validate_secret_key_format(secret_key):
        return isinstance(secret_key, str) and len(secret_key) == 40

    @staticmethod
    def validate_ssh_key_pair(key_pair_name, region, aws_key_id, aws_secret):
        ec2_client = boto3.client(
            "ec2", region_name=region,
            aws_access_key_id=aws_key_id,
            aws_secret_access_key=aws_secret
        )
        try:
            ec2_client.describe_key_pairs(KeyNames=[key_pair_name])
        except Exception:
            return False
        return True
