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

import base64
import json
import logging
import random
import shlex
import string
import yaml
from datetime import datetime

import six
from azure.core.exceptions import HttpResponseError
from azure.mgmt.compute.models import (
    HyperVGenerationTypes,
    Image,
    ImageOSDisk,
    ImageStorageProfile,
    OperatingSystemStateTypes,
    OperatingSystemTypes
)
from azure.mgmt.resource.resources.models import Deployment, DeploymentMode, DeploymentProperties
from msrestazure.tools import parse_resource_id
from six.moves import range

import clusterondemand.brightsetup
import clusterondemand.clustercreate
from clusterondemand import configuration, utils
from clusterondemand.bcm_version import BcmVersion
from clusterondemand.cidr import cidr, must_be_within_cidr
from clusterondemand.clustercreate import enable_cmd_debug_commands, generate_random_cluster_password
from clusterondemand.clusternameprefix import must_start_with_cod_prefix
from clusterondemand.exceptions import CODException, UserReportableException
from clusterondemand.ip import nth_ip_in_default_network
from clusterondemand.node_definition import NodeDefinition
from clusterondemand.ssh import clusterssh_ns
from clusterondemand.ssh_key import validate_ssh_pub_key
from clusterondemand.summary import SummaryType
from clusterondemand.wait_helpers import clusterwaiters_ns, wait_for_cluster_to_be_ready
from clusterondemandazure.azure_actions.storage import StorageAction
from clusterondemandazure.base import ClusterCommand
from clusterondemandazure.inbound_traffic_rule import ARM_format
from clusterondemandazure.summary import AzureSummaryGenerator
from clusterondemandconfig import ConfigNamespace, config
from clusterondemandconfig.configuration_validation import may_not_equal_none, requires_other_parameters_to_be_set

from .configuration import azurecommon_ns
from .constants import disk_setup
from .images import AzureImageSource, findimages_ns
from .template_builder import TemplateBuilder

# The list of supported storage SKUs was taken from Azure documentation:
# https://docs.microsoft.com/en-us/cli/azure/vm?view=azure-cli-latest#az-vm-create
SUPPORTED_DISK_SKUS = ["Standard_LRS", "Premium_LRS", "StandardSSD_LRS", "UltraSSD_LRS"]

config_ns = ConfigNamespace("azure.cluster.create", "cluster creation parameters")
config_ns.import_namespace(clusterondemand.configuration.clustercreate_ns)
config_ns.import_namespace(findimages_ns)
config_ns.override_imported_parameter("version", default="9.1")
config_ns.import_namespace(clusterondemand.configuration.cmd_debug_ns)
config_ns.import_namespace(clusterssh_ns)
config_ns.import_namespace(clusterwaiters_ns)
config_ns.import_namespace(azurecommon_ns)
config_ns.add_parameter(
    "name",
    help="Name of the cluster to create",
    validation=[may_not_equal_none, must_start_with_cod_prefix])
config_ns.override_imported_parameter("head_node_root_volume_size", default=42)
config_ns.add_parameter(
    "head_node_root_volume_type",
    advanced=True,
    choices=SUPPORTED_DISK_SKUS,
    default="StandardSSD_LRS",
    help="Storage type to use for Azure root volume")
config_ns.override_imported_parameter("node_type", default="Standard_D1_v2")
config_ns.override_imported_parameter("head_node_type", default="Standard_D1_V2")
config_ns.override_imported_parameter(
    "ssh_pub_key_path", validation=lambda p, c: validate_ssh_pub_key(p, c, allowed_types={"RSA": 2048})
)
config_ns.add_parameter(
    "vhd_url",
    advanced=True,
    help="The url for the source vhd for the server side copy")
config_ns.add_parameter(
    "head_node_image",
    help=("Single image selector statement for the head node image. Can either be an image "
          "URL, the name of that image or the name of the image set."),
)
config_ns.add_parameter(
    "network_cidr",
    default=cidr("10.142.0.0/16"),
    help="CIDR range of the VNet. The VNet Subnets must fall within this range. "
    "The widest allowed range is /16.",
    parser=cidr)
config_ns.add_parameter(
    "subnet_cidr",
    default=cidr("10.142.128.0/17"),
    help="CIDR range of the subnet. It must fall within the range specified by --network-cidr. ",
    parser=cidr,
    validation=must_be_within_cidr("network_cidr"))
config_ns.add_parameter(
    "head_node_ip",
    advanced=True,
    default=nth_ip_in_default_network(-2, "subnet_cidr"),
    help="The private IP address of the head node",
    help_varname="IP")
config_ns.add_switch_parameter(
    "skip_permission_verifications",
    help="Whether or not to skip verifying the credentials' access.")
config_ns.add_switch_parameter(
    "partial",
    help="Perform a partial cluster creation which relies on the resource group, storage account, "
         "and head node image to be already available")
config_ns.add_parameter(
    "storage_account",
    advanced=True,
    help="Storage account to use. By default it's generated or the existing one is used (if it's the only one)")

config_ns.add_parameter(
    "vnet_resource_group",
    advanced=True,
    help="Resource Group where the existing VNet is located",
    validation=requires_other_parameters_to_be_set(["vnet_network_name", "vnet_subnet_name"]),
)
config_ns.add_parameter(
    "vnet_network_name",
    advanced=True,
    help="Name of the Virtual Network to be used.",
    validation=requires_other_parameters_to_be_set(["vnet_resource_group", "vnet_subnet_name"]),
)
config_ns.add_parameter(
    "vnet_subnet_name",
    advanced=True,
    help="Name of the subnet to use.",
    validation=requires_other_parameters_to_be_set(["vnet_resource_group", "vnet_network_name"]),
)


def internal_subnet_id_validation(subnet_id_param, config):
    assert subnet_id_param.key == "internal_subnet_id"

    value = config[subnet_id_param.key]
    if value:
        try:
            parsed = parse_resource_id(value)
            config["vnet_resource_group"] = parsed["resource_group"]
            config["vnet_network_name"] = parsed["name"]
            config["vnet_subnet_name"] = parsed["child_name_1"]
        except Exception as e:
            raise CODException(f"'{value}' is not a valid Azure subnet ID") from e


config_ns.add_parameter(
    "internal_subnet_id",
    advanced=True,
    help="Azure ID for the existing subnet to be used. If set, a new VNet *will not* be created for this cluster. "
         "Instead, the head node will be attached to this existing subnet. This parameter combines "
         "--vnet-resource-group, --vnet-network-name and --vnet-subnet-name. See also --head-node-ip",
    validation=internal_subnet_id_validation,
)

config_ns.add_parameter(
    "resource_group",
    advanced=True,
    default=lambda _, config: ClusterCreate.default_resource_group_name(config["name"]),
    validation=must_start_with_cod_prefix,
    help="Resource group to use. All resources will be created in this resource group.",
)
config_ns.add_switch_parameter(
    "existing_rg",
    advanced=True,
    default=False,
    help="If set, COD will not try to create a resource group but instead just find the existing one. "
         "Use --resource-group to set a name.",
)

config_ns.add_switch_parameter(
    "create_public_ip",
    advanced=True,
    default=True,
    help="Create a public IP for the head node. Use --no-create-public-ip to skip creating one. In that case, to "
    "have access to the cluster, it will need to be created within an existing network that is accessible "
    "by the user. See --vnet-resource-group, --vnet-network-name and --vnet-subnet-name",
)


def run_command():
    ClusterCreate().run()


log = logging.getLogger("cluster-on-demand")


HR = "---------------------------------------------------------------------"


class ClusterCreate(ClusterCommand):

    def _get_head_node_name(self, cluster_name):
        return "%s-head-node" % cluster_name

    def generate_bright_conf(self):
        kwargs = dict()
        kwargs["cloud_type"] = "azure"

        if config["wlm"] != configuration.NO_WLM:
            kwargs["wlm"] = config["wlm"]
        else:
            kwargs["wlm"] = ""

        b = {
            "modules": {
                "brightsetup": {}
            }
        }

        bs = {
            "cloud_type": "azure",
            "bright": {
                "node_disk_setup_path": "/root/cm/disk-setup.xml",
                "wlm": kwargs["wlm"],
                "wlm_slot_count": 1,
                # None   type gets translated to 'None' string somewhere,
                # that's why need need empty string here for pbsproc_lic_server
                "pbspro_lic_server": "",
                "license": "",
                "hostname": str(self.head_node),  # otherwise it will end up as unicode:  u"xxxx"
                "master_compute_node": False,
                "password": config["cluster_password"],
                "node_count": config["nodes"],
            },
            "azure": {
                "region": self.location,
                "resource_group": self.resource_group,
                "storage_account": self.storage_account.name,
                "node_type": config["node_type"],
                "subscription_id": config["azure_subscription_id"],
                "nodes": {
                    "count": config["nodes"],
                    "storage": {  # default storage profiles for cloud nodes
                        "root-disk": 42,
                        "node-installer-disk": 2,
                    },
                    "base_name": "cnode",
                    "type": config["node_type"],
                },
                "client_id": config["azure_client_id"],
                "client_secret": config["azure_client_secret"],
                "tenant_id": config["azure_tenant_id"],
                "network_cidr": str(config["subnet_cidr"]),
                "head_node_ip": str(config["head_node_ip"])
            }
        }

        if BcmVersion(config["version"]) >= "9.0":
            if self.use_existing_vnet:
                bs["azure"]["network"] = {
                    "resource_group": config["vnet_resource_group"],
                    "vnet": config["vnet_network_name"],
                    "subnet": config["vnet_subnet_name"],
                }
            else:
                bs["azure"]["network"] = {
                    "resource_group": self.resource_group,
                    "vnet": f"vpc-{config['azure_location']}",
                    "subnet": f"vpc-{config['azure_location']}-subnet",
                }

        bs["bright"]["license"] = clusterondemand.brightsetup.get_license_dict()

        b["modules"]["brightsetup"] = bs

        return b

    def _create_storage_account(self):
        """
        Create a storage account and containers.

        The containers are used for saving image data and need to
        exist prior to server side copy and template deployment.
        """
        storage_action = StorageAction(self.azure_api)
        storage_action.create_storage_account(self.resource_group, self.storage_account.name, self.location)
        for container in ["images", "vhds"]:
            storage_action.create_container(container, self.storage_account.name, self.resource_group)

    def _server_side_copy(self):
        """
        Copy disk image from public bright storage account to the cluster's storage account.

        :return:
        """
        container = "images"
        blob_name = "%s-os-disk.vhd" % self.head_node
        vhd_url = self.head_node_image.uuid
        utils.cod_log(log, "Copying head node image from " + vhd_url, 7)
        storage_action = StorageAction(self.azure_api)
        storage_action.copy_blob(
            vhd_url,
            self.resource_group,
            self.storage_account.name,
            container,
            blob_name,
        )

    @staticmethod
    def default_resource_group_name(cluster_name):
        return "%s_cod_resource_group" % cluster_name

    @staticmethod
    def _shell_escape(text):
        return text.replace("'", "'\\''")

    def cloud_init_script(self):
        """
        Generate the cloud-init script to be ran on the head node.

        :return: String containing the cloud-init bash script
        """
        log.info("generating cloud-init script")
        bright_conf = self.generate_bright_conf()
        bright_conf = ClusterCreate._shell_escape(yaml.dump(bright_conf))

        cloud_init_script = """#!/bin/bash

        mkdir /root/.ssh/

        echo '%s' > /root/cm/cm-bright-setup.conf
        echo '%s' > /root/cm/disk-setup.xml
        """ % (bright_conf, disk_setup)

        if config["ssh_pub_key_path"]:
            with open(config["ssh_pub_key_path"]) as pub_key:
                cloud_init_script += """
                mkdir /root/.ssh/
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

        if config["cmd_debug"]:
            subsystems = config["cmd_debug_subsystems"]
            log.debug(f"Setting debug mode on CMDaemon for subsystems: '{subsystems}'")
            for command in enable_cmd_debug_commands(subsystems):
                cloud_init_script += command + "\n"

        if config["run_cm_bright_setup"]:
            if BcmVersion(config["version"]) < "8.2":
                cloud_init_script += "/cm/local/apps/cluster-tools/bin/cm-bright-setup " \
                                     "-c /root/cm/cm-bright-setup.conf --on-error-action abort"
            else:
                cloud_init_script += "/cm/local/apps/cm-setup/bin/cm-bright-setup " \
                                     "-c /root/cm/cm-bright-setup.conf --on-error-action abort"

        return cloud_init_script

    def generate_inbound_traffic_rules(self, inbound_rules):
        """
        convert CLI defined inbound traffic rules to the format expected by the AZURE API.
        """
        formatted_rules = []
        priority = 150
        for inbound_rule in inbound_rules:
            priority += 1
            formatted_rules.append(
                json.dumps(ARM_format(inbound_rule, priority), indent=4)
            )

        return ",\n".join(formatted_rules)

    def _validate_params(self):
        self._validate_cluster_name()
        self._validate_cluster_password()
        self._validate_access_credentials()
        self._validate_location()
        self._validate_vmsize()
        self._validate_blob()

    def on_error(self, r_client):
        if config["on_error"] == "cleanup":
            async_removal = r_client.resource_groups.begin_delete(self.resource_group)
            log.info("Resource group removal initiated.")
            async_removal.wait()
        else:
            log.info("Failed environment was kept and will have to be deleted manually.")

    def verify_api_credentials(self):
        """
         Creates a temporary resource group and virtual network in order to make sure the provided API
         credentials have all required permissions.
        """
        random_resource_name = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in
            range(20)
        )
        log.info("Temporary azure resources will be created (resource group: %s) in order"
                 " to verify that the API credentials have the required permissions, this"
                 " can take a few minutes. You can skip this step by specifying the following"
                 " flag: '--skip-permission-verifications'", random_resource_name)
        try:
            self.azure_api.resource_client.resource_groups.create_or_update(
                random_resource_name,
                {"location": config["azure_location"]}
            )

            try:
                self.azure_api.network_client.virtual_networks.begin_create_or_update(
                    random_resource_name,
                    random_resource_name,
                    {"location": config["azure_location"],
                     "properties": {
                         "addressSpace": {"addressPrefixes": ["10.10.10.0/24"]}}
                     }
                )
                # The IP address here is arbitrary and was just added to satisfy Azure API
                # requirements.
            except HttpResponseError as e:
                log.debug(e.message)
                raise UserReportableException(
                    "Insufficient write access: Not enough permissions to create a virtual network."
                )

            log.info(
                "Credentials are valid and have read/write authorizations.")
            async_removal = self.azure_api.resource_client.resource_groups.begin_delete(
                random_resource_name)
            log.debug("Cleanup removal initiated.")
            async_removal.wait()

        except HttpResponseError as e:
            log.debug(e.message)
            raise UserReportableException(
                "Insufficient write access: unable to create a resource group."
            )

    def create_resource_group(self):
        utils.cod_log(log, "Creating resource group %s" % self.resource_group, 2)
        try:
            if not self.azure_api.resource_client.resource_groups.check_existence(self.resource_group):
                self.azure_api.resource_client.resource_groups.create_or_update(
                    self.resource_group,
                    {
                        "location": self.location,
                        "tags": {
                            "BCM Resource": True,
                            "BCM Created at": datetime.utcnow().isoformat() + "Z",  # fix missing timezone
                            "BCM Created by": utils.get_user_at_fqdn_hostname(),
                            "BCM Cluster": self.head_node,
                            "BCM Bursting": "on-demand",
                        }
                    }
                )
            else:
                raise UserReportableException(
                    "The resource group '%s' already exists." % self.resource_group
                )
        except UserReportableException as e:
            raise e
        except HttpResponseError as e:
            self.on_error(self.azure_api.resource_client)
            raise CODException("Template deployment failed: %s" % str(e), caused_by=e)
        except Exception as e:
            self.on_error(self.azure_api.resource_client)
            raise CODException("Template deployment failed: %s" % str(e), caused_by=e)

    def server_side_copy_head_node_image_blob(self):
        """
        Copy disk image from public bright storage account to the cluster's storage account.

        :return: blob_url
        """
        self._server_side_copy()
        blob_url = "https://{storage_account_name}.blob.core.windows.net/images/{head_node_name}-os-disk.vhd".format(
            storage_account_name=self.storage_account.name,
            head_node_name=self.head_node
        )
        return blob_url

    def delete_head_node_image_blob(self):
        storage_action = StorageAction(self.azure_api)
        storage_action.delete_blob(self.resource_group,
                                   self.storage_account.name,
                                   "images",
                                   f"{self.head_node}-os-disk.vhd")

    def create_head_node_image_from_blob(self, blob_url):
        """
        Creates an image from a azure disk (VHD) given its url
        """
        img_name = "{head_node_name}-os-disk".format(head_node_name=self.head_node)
        img_params = Image(
            location=self.location,
            tags={"BCM Resource": True},
            storage_profile=ImageStorageProfile(
                os_disk=ImageOSDisk(
                    os_type=OperatingSystemTypes.linux,
                    os_state=OperatingSystemStateTypes.generalized,
                    blob_uri=blob_url,
                    caching="ReadOnly",
                )
            ),
            hyper_v_generation=HyperVGenerationTypes.V1
        )

        creation_successful = False
        current_attempt = 0
        MAX_ATTEMPTS = 3
        log.info("Creating Azure Image resource '%s' from blob %s", img_name, blob_url)
        while current_attempt < MAX_ATTEMPTS and not creation_successful:
            try:
                create_img_future = self.azure_api.compute_client.images.begin_create_or_update(
                    resource_group_name=self.resource_group,
                    image_name=img_name,
                    parameters=img_params)
                future = create_img_future
                future.wait()
                creation_successful = True
            except HttpResponseError as e:
                if blob_url in e.message:
                    log.debug("Failed to create the headnode image, retrying...")
                    current_attempt += 1
                    continue
                raise CODException("Failed to create the headnode image", caused_by=e)

    def check_resource_group_usability(self):
        """
        Verifies the presence of a reusable resource group
        """
        if self.azure_api.resource_client.resource_groups.check_existence(self.resource_group):
            # Checking whether a storage account already exists or not
            rg_storage_accs = [a.name for a in (self.azure_api.storage_client.storage_accounts.
                               list_by_resource_group(self.resource_group))]
            if self.storage_account is None:
                if len(rg_storage_accs) == 1:
                    self.storage_account = StorageAccount(rg_storage_accs[0])
                    log.debug(f"Found the only storage account '{self.storage_account.name}'"
                              f" associated with resource group '{self.resource_group}'")
                elif not rg_storage_accs:
                    raise CODException(
                        f"Resource group '{self.resource_group}' doesn't have any storage accounts."
                        f" If you want to create a cluster in the existing resource group use"
                        f" '--existing-rg --resource-group {self.resource_group}' parameters"
                    )
                else:
                    raise CODException(
                        f"Resource group '{self.resource_group}' has multiple storage accounts:"
                        f"{', '.join(rg_storage_accs)}. Please, specify which one you want to use"
                        f" using --storage-account parameter"
                    )
            elif self.storage_account.name not in rg_storage_accs:
                raise CODException(f"Resource group '{self.resource_group}' doesn't have specified"
                                   f" storage account '{self.storage_account.name}")

            head_node_image_name = f"{self.head_node}-os-disk"
            try:
                self.azure_api.compute_client.images.get(self.resource_group, head_node_image_name)
            except HttpResponseError as e:
                raise CODException(f"Resource group '{self.resource_group}' doesn't have"
                                   f" the head node image '{head_node_image_name}'", caused_by=e)
        else:
            raise CODException(f"The resource group for the Cluster '{config['name']}' does not exist")

    def run(self):
        self._storage_client = None
        self._compute_client = None
        self._resource_client = None
        self._network_client = None

        self.head_node = self._get_head_node_name(config["name"])
        self._validate_params()

        log.info("Cluster Create ")

        self.storage_account = None
        if config["storage_account"]:
            self.storage_account = StorageAccount(config["storage_account"])
        elif not config["partial"]:
            self.storage_account = StorageAccount.storage_account_for_cluster(config["name"])

        self.resource_group = config["resource_group"]
        self.deployment_name = "%s-azure-deployment" % config["name"]

        self.location = config["azure_location"]
        inbound_rules = self.generate_inbound_traffic_rules(config["inbound_rule"])

        if config["vhd_url"]:
            if config["head_node_image"]:
                raise CODException("--vhd-url and --head-node-image cannot be used at the same time")
            # For compatiblity with the existing vhd_url parameter
            config["head_node_image"] = config["vhd_url"]

        self.head_node_image = AzureImageSource.pick_head_node_image_using_options(config)

        self.use_existing_vnet = False
        if config["vnet_resource_group"]:
            if BcmVersion(config["version"]) >= "9.0":
                self.use_existing_vnet = True
            else:
                parameter_values = ", ".join(
                    f"{config.item_repr(key)}"
                    for key in ["vnet_resource_group", "vnet_network_name", "vnet_subnet_name"]
                )
                log.warning(
                    f"Bright versions below 9.0 don't support using an existing VNet. "
                    f"The parameters {parameter_values} will be ignored. "
                )

        generator = AzureSummaryGenerator(config,
                                          SummaryType.Proposal,
                                          head_node_definition=NodeDefinition(1, config["head_node_type"]),
                                          head_image=self.head_node_image,
                                          node_definition=NodeDefinition(config["nodes"], config["node_type"]),
                                          region=self.location)
        generator.print_summary(log.info)

        if self.use_existing_vnet:
            subnet = self.azure_api.network_client.subnets.get(
                config["vnet_resource_group"],
                config["vnet_network_name"],
                config["vnet_subnet_name"],
            )

            log.info(
                f"Cluster will use existing Virtual Network {config['vnet_network_name']}/{config['vnet_subnet_name']} "
                f"on resource group {config['vnet_resource_group']}"
            )

            self.existing_subnet_id = subnet.id
            config["subnet_cidr"] = cidr(subnet.address_prefix)

            if not config.is_item_set_explicitly("head_node_ip"):
                config["head_node_ip"] = config["subnet_cidr"][-2]

        if config["head_node_ip"] not in config["subnet_cidr"]:
            # We can't put this validation on the parameters because we have to check if it's an existing VPC first
            raise CODException(
                f"Parameter {config.item_repr('head_node_ip')} is not in the specified subnet. "
                f"Available range: {config['subnet_cidr']}."
            )

        if config["ask_to_confirm_cluster_creation"]:
            utils.confirm_cluster_creation(num_clusters=1)

        if config["dry_run"]:
            log.info("Running in dry-run mode. Cluster will not be created.")
            return

        if not config["skip_permission_verifications"]:
            self.verify_api_credentials()

        if (
            config["existing_rg"] and
            not self.azure_api.resource_client.resource_groups.check_existence(self.resource_group)
        ):
            raise CODException(
                f"Resource group {self.resource_group} does not exist. "
                f"Unset --existing-rg if you wish that COD creates it."
            )

        if not config["partial"]:
            if not config["existing_rg"]:
                self.create_resource_group()
            self._create_storage_account()
            blob_url = self.server_side_copy_head_node_image_blob()
            self.create_head_node_image_from_blob(blob_url)
            self.delete_head_node_image_blob()
        else:
            self.check_resource_group_usability()

        utils.cod_log(log, "Building deployment template", 45)
        tb = TemplateBuilder(
            head_node_name=self.head_node,
            head_node_flavour=config["head_node_type"],
            storage_account=self.storage_account.name,
            region=self.location,
            custom_data=_b64encode(self.cloud_init_script()),
            user_random_password=generate_random_cluster_password(length=50),
            head_node_ip=str(config["head_node_ip"]),
            network_cidr=str(config["network_cidr"]),
            subnet_cidr=str(config["subnet_cidr"]),
            head_node_root_volume_size=config["head_node_root_volume_size"],
            head_node_root_volume_type=config["head_node_root_volume_type"],
            image_name=self.head_node_image.name,
            image_creation_date=str(self.head_node_image.created_at),
            inbound_rules=inbound_rules,
        )
        template = tb.build()

        deployment_parameters = {}
        if self.use_existing_vnet:
            deployment_parameters["subnet_id"] = {"value": self.existing_subnet_id}
            deployment_parameters["create_new_vnet"] = {"value": "false"}

        deployment_parameters["create_public_ip"] = {"value": str(config["create_public_ip"]).lower()}

        deployment_properties = DeploymentProperties(
            mode=DeploymentMode.incremental,
            template=template,
            parameters=deployment_parameters
        )

        utils.cod_log(log, "Creating and deploying Head node", 85)

        try:
            deployment_async_operation = self.azure_api.resource_client.deployments.begin_create_or_update(
                resource_group_name=self.resource_group,
                deployment_name=self.deployment_name,
                parameters=Deployment(properties=deployment_properties)
            )
            deployment_async_operation.wait()
        except HttpResponseError as e:
            if "StaticPublicIPCountLimitReached" in e.message:
                raise UserReportableException(e.message)
            if "SkuNotAvailable" in e.message:
                raise UserReportableException(
                    "The requested vmsize: '{vmsize}' is not available in the location: "
                    "'{location}' temporarily, please select a different region or vmsize.".format(
                        vmsize=config["head_node_type"],
                        location=config["azure_location"]
                    )
                )
            if "DeploymentFailed" in e.message:
                try:
                    for operation in self.azure_api.resource_client.deployment_operations.list(
                        resource_group_name=self.resource_group,
                        deployment_name=self.deployment_name
                    ):
                        if operation.properties.status_code.upper() != "OK":
                            resource_name = operation.properties.target_resource.resource_name
                            error_code = operation.properties.status_message.error.code
                            error_message = operation.properties.status_message.error.message
                            log.error(f"Deployment error for resource {resource_name}: ({error_code}) {error_message}")
                except Exception as inner_e:
                    log.error(f"Error while diagnosing deployment failure: {inner_e}")

            self.on_error(self.azure_api.resource_client)
            raise CODException("Template deployment failed: %s" % e.message, caused_by=e)
        except Exception as e:
            self.on_error(self.azure_api.resource_client)
            raise CODException("Template deployment failed: %s" % str(e), caused_by=e)

        instance_id = self.azure_api.compute_client.virtual_machines.get(
            self.resource_group, "%s" % self.head_node
        ).vm_id

        if config["create_public_ip"]:
            public_ip = self.azure_api.network_client.public_ip_addresses.get(
                self.resource_group, "head-node-public-ip"
            ).ip_address
            log.info("Head node IP: %s" % public_ip)

            wait_for_cluster_to_be_ready(config, public_ip, config["version"])
        else:
            public_ip = "N/A"
            log.info("Cluster was created without a public IP. COD cannot wait for cmdaemon to be ready.")
            log.info(f"Head node private IP: {config['head_node_ip']}")

        utils.cod_log(log, "Deployment finished successfully.", 100)

        generator = AzureSummaryGenerator(config,
                                          SummaryType.Overview,
                                          instance_id=instance_id,
                                          public_ip=public_ip)
        generator.print_summary(log.info)


def _b64encode(string):
    if six.PY3:
        return base64.b64encode(string.encode("utf-8")).decode("utf-8")
    else:
        return base64.b64encode(string)


class StorageAccount(object):
    """Represents an Azure Storage account."""

    N_RANDOM_CHARS = 6
    MAX_STORAGE_ACCOUNT_NAME_LEN = 24
    ALLOWED_NAME_CHARACTERS = string.ascii_lowercase + string.digits

    @classmethod
    def storage_account_for_cluster(cls, cluster_name):
        """Factory method that generates an instance with the proper name."""
        return cls(cls._name_for_storage_account(cluster_name))

    def __init__(self, name):
        self.name = name

    @classmethod
    def _name_for_storage_account(cls, cluster_name):
        full_name = cluster_name + "storageaccount"
        clean_name_chars = [ch for ch in full_name.lower() if ch in cls.ALLOWED_NAME_CHARACTERS]
        random_chars = [random.choice(cls.ALLOWED_NAME_CHARACTERS) for _ in range(cls.N_RANDOM_CHARS)]
        return "".join(clean_name_chars[:cls.MAX_STORAGE_ACCOUNT_NAME_LEN - cls.N_RANDOM_CHARS] + random_chars)
