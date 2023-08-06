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

from azure.core.exceptions import ClientAuthenticationError

from clusterondemand.exceptions import UserReportableException
from clusterondemand.paramvalidation import ParamValidator
from clusterondemandazure.azure_actions.credentials import AzureApiHelper
from clusterondemandazure.paramvalidation import AZUREParamValidator
from clusterondemandconfig import config

log = logging.getLogger("cluster-on-demand")


class ClusterCommand(object):
    """Base class for all Azure cluster commands.

    This class only contains non-public validator methods that are intended to be used by
    descendant classes to validate user input. The general contract for all these methods is
    to perform various input sanitization checks, raising an Exception in the case of a failed
    check. If the check passes the _validate_xxx methods will simply return control to the
    caller with no return value.
    """

    def __init__(self):
        self.azure_api = AzureApiHelper.from_config(config)

    def _validate_cluster_name(self):
        ParamValidator.validate_cluster_name(config["name"])

    def _validate_cluster_password(self):
        if (isinstance(config["cluster_password"], str) and
                not AZUREParamValidator.validate_password(config["cluster_password"])):
            raise UserReportableException(
                "Cluster Password '%s' does not match proper format, the password should "
                "be at least 8 characters long." % config["cluster_password"]
            )

    def _validate_access_credentials(self):
        ParamValidator.validate_uuid_format(config["azure_tenant_id"], "Tenant ID does not match the proper format")
        ParamValidator.validate_uuid_format(config["azure_client_id"], "Client ID does not match the proper format")

        try:
            self.azure_api.get_credential()
            # We only validate the credentials once we call the API.
            # This means that we need to make an actual API call in which we use the results.
            list(self.azure_api.subscription_client.subscriptions.list())
        except ClientAuthenticationError:
            raise UserReportableException(
                "Azure API Authentication failed: provided credentials are invalid."
            )

    def _validate_location(self):
        if not AZUREParamValidator.validate_location(
                self.azure_api,
                config["azure_location"]
        ):
            raise UserReportableException(
                "Region %s does not exist." % config["azure_location"]
            )

    def _validate_vmsize(self):
        if not AZUREParamValidator.validate_vmsize(
                self.azure_api,
                config["azure_location"],
                config["head_node_type"],
        ):
            raise UserReportableException(
                "VMSize %s does not exist in location %s." %
                (config["head_node_type"], config["azure_location"]))

        if not AZUREParamValidator.validate_vmsize(
                self.azure_api,
                config["azure_location"],
                config["node_type"]
        ):
            raise UserReportableException(
                "VMSize %s does not exist in location %s." %
                (config["node_type"], config["azure_location"])
            )

    def _validate_blob(self):
        if (config["vhd_url"] and
                not AZUREParamValidator.validate_custom_blob(config["vhd_url"])):
            raise UserReportableException("VHD Blob specified does not exist or is unreachable.")
