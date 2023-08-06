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

import fnmatch
import logging
import re

from azure.core.exceptions import HttpResponseError

import clusterondemand.clustercreate
from clusterondemand.codoutput.sortingutils import SortableData
from clusterondemand.exceptions import UserReportableException
from clusterondemandazure.base import ClusterCommand
from clusterondemandconfig import ConfigNamespace, config

from .configuration import azurecommon_ns

log = logging.getLogger("cluster-on-demand")

ALL_COLUMNS = [
    ("cluster_name", "Cluster Name"),
    ("head_node_name", "Head node name"),
    ("public_ip", "Public IP"),
    ("location", "Location"),
    ("head_node_vmsize", "Head node Vmsize"),
    ("head_node_cpu", "Head node CPU cores"),
    ("head_node_ram", "Head node Ram (mb)"),
    ("created", "Image Created"),
    ("image_name", "Image Name"),
]

config_ns = ConfigNamespace("azure.cluster.list", help_section="list output parameters")
config_ns.import_namespace(clusterondemand.configuration.clusterlist_ns)
config_ns.import_namespace(azurecommon_ns)
config_ns.add_enumeration_parameter(
    "sort",
    choices=[column[0] for column in ALL_COLUMNS],
    default=["created"],
    help="Sort results by one (or two) of the columns")
config_ns.add_enumeration_parameter(
    "columns",
    choices=[column[0] for column in ALL_COLUMNS],
    help="Provide space separated set of columns to be displayed")
config_ns.add_repeating_positional_parameter(
    "filters",
    default=["*"],
    require_value=True,
    help="Cluster names or patterns to be listed. Default: all clusters. Wildcards are supported (e.g: prefix-*)")


def run_command():
    ClusterList().run()


class ClusterList(ClusterCommand):

    def run(self):
        try:
            self._validate_params()
        except HttpResponseError as e:
            if "SubscriptionNotFound" in e.error.code:
                raise UserReportableException(str(e))
            raise e

        rows = []
        global_vmsizes = {}
        cod_resource_groups = get_cod_resource_groups(self.azure_api.resource_client, config["filters"])

        for r_group in cod_resource_groups:
            rows.append(get_cluster_data(self.azure_api, r_group, global_vmsizes))

        cols_id = config["columns"]
        if not cols_id:
            cols_id = [column[0] for column in ALL_COLUMNS]

        table = SortableData(
            all_headers=ALL_COLUMNS,
            requested_headers=cols_id,
            rows=rows
        )
        table.sort(*config["sort"])

        print(table.output(output_format=config["output_format"]))

    def _validate_params(self):
        self._validate_access_credentials()


def get_cluster_data(azure_api, r_group, global_vmsizes):
    """
    Return list containing cluster information of a given resource group.

    :param azure_api: instance of AzureApiHelper
    :param r_group: resource group object
    :param global_vmsizes: global dictionary mapping
    :return: cluster information in the following format:
        [
            cluster_name,
            head_node_name,
            public_ip,
            location,
            vm_size,
            cpu_cores,
            ram,
            image_creation_date,
            image_name,
        ]
    """
    missing_resources = []
    try:
        public_ip = azure_api.network_client.public_ip_addresses.get(
            r_group.name, "head-node-public-ip"
        ).ip_address
    except Exception:
        missing_resources.append("public ip")
        public_ip = "?"

    cluster_name = name_from_r_group(r_group.name)
    head_node_name = "%s-head-node" % cluster_name

    try:
        head_node = azure_api.compute_client.virtual_machines.get(
            r_group.name, "%s" % head_node_name
        )

        specs = get_location_vmsize_details(
            azure_api.compute_client,
            global_vmsizes,
            r_group.location,
            head_node.hardware_profile.vm_size
        )
        vm_size = head_node.hardware_profile.vm_size
        cpu_cores = specs["Cpu cores"]
        ram = specs["Ram (mb)"]
        image_creation_date = head_node.tags["image_creation_date"]
        image_name = head_node.tags["image_name"]

    except Exception:
        missing_resources.append("head node")

        vm_size = "?"
        cpu_cores = -1
        ram = -1
        image_creation_date = "?"
        image_name = "?"

    if missing_resources:
        log.warning("Some resources %s seem to be missing in %s, this is probably sign of a "
                    "broken deployment. You can remove the cluster by running : "
                    "cm-cod-azure cluster delete %s",
                    missing_resources, cluster_name, cluster_name)

    return [
        name_from_r_group(r_group.name),
        head_node_name,
        public_ip,
        r_group.location,
        vm_size,
        cpu_cores,
        ram,
        image_creation_date,
        image_name,
    ]


def get_location_vmsize_details(compute_client, global_vmsizes, location, vmsize_name):
    """
    Return details of virtual machine size.

    Checks if vmsize already exists in the global dictionary [global_vmsizes]
    then returns its properties
    Otherwise, pulls that vmsize's information, adds them to the global dictionary
    then returns its properties

    :param compute_client: azure sdk compute client
    :param global_vmsizes: global dictionary mapping vmsizes and their properties
    :param location: location of the given vmsize
    :param vmsize_name: name of the vmsize
    :return: a dictionary of the vmsize information in the following format :
        {
            "Cpu cores": number_of_cores,
            "Ram (mb)": memory_in_mb,
        }
    """
    if vmsize_name in global_vmsizes:
        return global_vmsizes[vmsize_name]

    paged_vmsizes = compute_client.virtual_machine_sizes.list(location=location)
    vmsize = next(paged_vmsizes)
    while vmsize:
        if vmsize.name in vmsize_name:
            global_vmsizes[vmsize_name] = {
                "Cpu cores": vmsize.number_of_cores,
                "Ram (mb)": vmsize.memory_in_mb,
            }
            return global_vmsizes[vmsize_name]
        try:
            vmsize = next(paged_vmsizes)
        except GeneratorExit:
            break


def name_from_r_group(r_group_name):
    """
    Obtain name of resource group.

    :param r_group_name: resource group name
    :return: extracted cluster name from group name
    """
    suffix_length = 19  # = len("_cod_resource_group")
    return r_group_name[:-suffix_length]


def get_cod_resource_groups(resource_client, patterns):
    """
    Return COD resource groups.

    :param resource_client: azure sdk resource client
    :return: list of resource groups containing cod-azure clusters
    """

    regexes = [fnmatch.translate(f"{p}_cod_resource_group") for p in patterns]

    r_groups = [
        item for item in resource_client.resource_groups.list()
        if any(re.match(r, item.name) for r in regexes)
    ]
    return r_groups
