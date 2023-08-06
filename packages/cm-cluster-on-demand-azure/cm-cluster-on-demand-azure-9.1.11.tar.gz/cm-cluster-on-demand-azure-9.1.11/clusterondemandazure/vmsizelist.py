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

import clusterondemand
from clusterondemand.codoutput.sortingutils import SortableData
from clusterondemand.exceptions import CODException
from clusterondemandconfig import ConfigNamespace, config

from .azure_actions.credentials import AzureApiHelper
from .configuration import azurecommon_ns

columns = [
    ("location", "Location"),
    ("vmsizes", "VMSizes"),
    ("ram", "Ram (GB)"),
    ("cpu", "CPU Cores"),
    ("max_disks", "Max Data Disk")
]
log = logging.getLogger("cluster-on-demand")


HR = "---------------------------------------------------------------------"


config_ns = ConfigNamespace("azure.vmsize.list", "list output parameters")
config_ns.import_namespace(clusterondemand.configuration.clusterlist_ns)
config_ns.import_namespace(azurecommon_ns)
config_ns.add_enumeration_parameter(
    "sort",
    default=["location"],
    choices=[col[0] for col in columns],
    help="Column according to which the table should be sorted (asc order)."
)
config_ns.add_parameter(
    "location",
    help="Only show vmsizes for this location."
)
config_ns.override_imported_parameter(
    "output_format",
    choices=["table", "json"],
    help_varname=None,
)


def run_command():
    return VMSizesList().run()


class VMSizesList(object):

    @staticmethod
    def list_locations(azure_api):
        """Return list of available locations in an Azure subscription."""
        locations = []
        paged_location = azure_api.subscription_client.subscriptions.list_locations(azure_api.subscription_id)

        next_page = next(paged_location)
        while next_page:
            if not isinstance(next_page, list):
                next_page = [next_page]
            for location in next_page:
                locations.append(location.name)
            try:
                next_page = next(paged_location)
            except (GeneratorExit, StopIteration):
                break
        return locations

    @staticmethod
    def is_valid_location(azure_api, location):
        """
        Check whether or not the provided location is a valid Azure location.

        :param azure_api: instance of AzureApiHelper
        :param location: Location provided via CLI arg
        :return:
        """
        return location in VMSizesList.list_locations(azure_api)

    @staticmethod
    def get_vm_specs(resource):
        """
        Get the hardware specs of a virtual machine from a Resource SKU.
        """

        for capability in resource.capabilities:
            if capability.name == "vCPUs":
                number_of_cores = capability.value
            elif capability.name == "MemoryGB":
                memory_in_gb = capability.value
            elif capability.name == "MaxDataDiskCount":
                max_data_disk_count = capability.value

        return {
            "Cpu cores": number_of_cores,
            "Ram (GB)": memory_in_gb,
            "Max disk count": max_data_disk_count,
        }

    def get_location_vmsizes(self, azure_api, location):
        """
        Create location<->vmsizes mapping as well as vmsizes<->specs one.

        :param azure_api: instance of AzureApiHelper
        :param location:
        :return: List of VMSizes available in the given Location
        """
        vmsizes = []

        location_filter = f"location eq '{location}'" if location else None
        resource_skus = azure_api.compute_client.resource_skus.list(filter=location_filter)

        for resource in resource_skus:
            if resource.resource_type != "virtualMachines":
                continue

            vmsizes.append(resource.name)
            if resource.name not in self.vmsize_to_specs_mapping:
                self.vmsize_to_specs_mapping[resource.name] = VMSizesList.get_vm_specs(resource)

        return sorted(vmsizes)

    def generate_location_to_vmsize_mapping(self, location):
        """
        Generate a dictionary mapping vmsizes available in the given location.

        :param location:
        :return:
        """
        mapping = {}
        if location:
            log.info("Listing available VMSizes in %s", location)
            mapping[location] = self.get_location_vmsizes(self.azure_api, location)
        else:
            log.info("Listing available VMSizes for all locations")
            for location in self.list_locations(self.azure_api):
                mapping[location] = self.get_location_vmsizes(self.azure_api, location)
        return mapping

    def output_json_file(self):
        """Print all mappings in a json file."""
        json_mapping = json.dumps(
            {"size": self.vmsize_to_specs_mapping, "regions": self.location_to_vmsize_mapping},
            indent=4,
            sort_keys=True,
        )
        print(json_mapping)

    def output_prettytable(self, all_columns):
        """Print all mappings in a Table."""
        location_to_vmsize = []
        for key, value in six.iteritems(self.location_to_vmsize_mapping):
            for val in value:
                location_to_vmsize.append([
                    key,
                    val,
                    self.vmsize_to_specs_mapping[val]["Ram (GB)"],
                    self.vmsize_to_specs_mapping[val]["Cpu cores"],
                    self.vmsize_to_specs_mapping[val]["Max disk count"]
                ])
        cols_id = [column[0] for column in all_columns]
        table = SortableData(
            all_headers=all_columns,
            requested_headers=cols_id,
            rows=location_to_vmsize
        )
        table.sort(*config["sort"])
        print(table.output(output_format=config["output_format"]))

    def run(self):
        location = config["location"]

        self.azure_api = AzureApiHelper.from_config(config)

        if location and not self.is_valid_location(self.azure_api, location):
            raise CODException(
                "Location [%s] is not a valid azure location "
                "or is not available for this subscription"
                "Available locations are : "
                "%s " % (location, ", ".join(self.list_locations(self.azure_api)))
            )

        self.vmsize_to_specs_mapping = {}
        self.location_to_vmsize_mapping = self.generate_location_to_vmsize_mapping(location)

        if config["output_format"] == "json":
            self.output_json_file()
        elif config["output_format"] == "table":
            self.output_prettytable(columns)
