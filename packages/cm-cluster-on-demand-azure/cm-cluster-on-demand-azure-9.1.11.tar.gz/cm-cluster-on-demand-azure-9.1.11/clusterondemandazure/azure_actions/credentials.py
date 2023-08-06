#
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

import logging
from functools import lru_cache

import requests.exceptions  # requests is a dependency of azure
import tenacity
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.subscription import SubscriptionClient
from msrest.exceptions import AuthenticationError

log = logging.getLogger("cluster-on-demand")


class AzureApiHelper:
    def __init__(self, client_id, client_secret, tenant_id, subscription_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.subscription_id = str(subscription_id)

        self._silence_http_logs()

    @staticmethod
    @lru_cache()
    def _silence_http_logs():
        logging.getLogger("msrest").setLevel(logging.WARNING)
        logging.getLogger("azure.mgmt").setLevel(logging.WARNING)
        logging.getLogger("requests_oauthlib").setLevel(logging.WARNING)

    @classmethod
    def from_config(cls, config):
        return cls(
            client_id=config["azure_client_id"],
            client_secret=config["azure_client_secret"],
            tenant_id=config["azure_tenant_id"],
            subscription_id=config["azure_subscription_id"],
        )

    @property
    @lru_cache()
    def storage_client(self):
        return StorageManagementClient(
            self.get_credential(),
            self.subscription_id,
        )

    @property
    @lru_cache()
    def network_client(self):
        return NetworkManagementClient(
            self.get_credential(),
            self.subscription_id,
        )

    @property
    @lru_cache()
    def resource_client(self):
        return ResourceManagementClient(
            self.get_credential(),
            self.subscription_id,
        )

    @property
    @lru_cache()
    def compute_client(self):
        return ComputeManagementClient(
            self.get_credential(),
            self.subscription_id,
        )

    @property
    @lru_cache()
    def subscription_client(self):
        return SubscriptionClient(
            self.get_credential(),
        )

    @lru_cache()
    @tenacity.retry(
        wait=tenacity.wait_exponential(),
        stop=tenacity.stop_after_delay(60),
        retry=tenacity.retry_if_exception(
            lambda e: (
                isinstance(e, (requests.exceptions.ConnectionError, requests.exceptions.SSLError))
                or (
                    isinstance(e, AuthenticationError)
                    and isinstance(e.inner_exception, requests.exceptions.ConnectionError)  # pylint: disable=no-member
                )
            )
        ),
        reraise=True,
        before_sleep=tenacity.before_sleep_log(log, logging.DEBUG),
    )
    def get_credential(self):
        return ClientSecretCredential(
            client_id=self.client_id,
            client_secret=self.client_secret,
            tenant_id=self.tenant_id,
        )
