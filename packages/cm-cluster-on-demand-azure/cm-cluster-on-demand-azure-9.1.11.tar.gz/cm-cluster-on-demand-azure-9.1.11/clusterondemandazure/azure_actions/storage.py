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
import asyncio
import logging
import math
import time
from datetime import datetime

from azure.core.exceptions import HttpResponseError, ServiceRequestError
from azure.mgmt.storage.models import BlobContainer, Kind, Sku, SkuName, StorageAccountCreateParameters
from azure.storage.blob import BlobClient
from azure.storage.blob.aio import BlobClient as AioBlobClient
from tenacity import retry
from tenacity.retry import retry_if_exception_type
from tenacity.stop import stop_after_delay
from tenacity.wait import wait_random_exponential

from clusterondemand.exceptions import CODException
from clusterondemand.utils import report_progress

log = logging.getLogger("cluster-on-demand")


class StorageAction:
    def __init__(self, azure_api):
        self.azure_api = azure_api

    @staticmethod
    def get_blob_metadata(blob_url, credential=None):
        blob_client = BlobClient.from_blob_url(blob_url, credential)
        blob_properties = blob_client.get_blob_properties()
        return blob_properties.metadata

    def create_storage_account(self, resource_group, storage_account, location):
        log.info("Creating storage account %s", storage_account)
        create_parameters = StorageAccountCreateParameters(sku=Sku(name=SkuName.standard_ragrs),
                                                           kind=Kind.storage,
                                                           tags={"BCM Resource": True},
                                                           location=location)
        self.azure_api.storage_client.storage_accounts.begin_create(resource_group,
                                                                    storage_account,
                                                                    create_parameters).wait()

    def create_container(self, container, storage_account, resource_group):
        log.debug(f"Creating container {container} in {storage_account}.")
        self.azure_api.storage_client.blob_containers.create(
            resource_group,
            storage_account,
            container,
            BlobContainer(),
        )

    def copy_blob(self, src_url, resource_group, storage_account, container, blob):
        start_time = time.time()
        log.info(f"Copying {src_url} to {storage_account}/{container}/{blob}")

        blob_client = self._get_blob_client(resource_group, storage_account, container, blob)
        PageBlobCopier.copy_blob(blob_client, src_url)

        elapsed = time.time() - start_time
        log.info(f"Copy completed in {int(elapsed // 60):02}:{int(elapsed % 60):02} min")

    def delete_blob(self, resource_group, storage_account, container, blob):
        log.info(f"Deleting blob {storage_account}/{container}/{blob}")
        blob_client = self._get_blob_client(resource_group, storage_account, container, blob)
        blob_client.delete_blob()

    def _get_blob_client(self, resource_group, storage_account, container, blob):
        # For authentication with the blob service we need to use a
        # shared key that is associated with the storage account.
        result = self.azure_api.storage_client.storage_accounts.list_keys(resource_group, storage_account)
        account_key = result.keys[0].value

        blob_url = f"https://{storage_account}.blob.core.windows.net/{container}/{blob}"
        return BlobClient.from_blob_url(blob_url, account_key)


class PageBlobCopier:
    @staticmethod
    def copy_blob(blob_client, src_url):
        """
        Copy of a PageBlob from one Azure container to another Azure container.

        Implementation is based on AzCopy, a command-line tool that moves data into and out of
        Azure Storage. For a PageBlob AzCopy creates a destination blob with the right size that is
        initially filled with zeros. Then the PageBlob is overwritten with the contents of the
        original PageBlob in 4MiB sections. The advantage of this approach is that each transfer is
        independent and can be performed concurrently.

        :param blob_client: The client for the destination blob. The blob does not need to exist.
        :param src_url: The url of the source blob. This url needs to be public or contain a SAS token.
        """
        blob_copier = PageBlobCopier(blob_client, src_url)
        if not blob_client.exists():
            blob_copier._create_blob()

        try:
            asyncio.run(blob_copier._copy_blob_contents())
        except Exception as e:
            raise CODException("Problem while copying the headnode image, please try again later.") from e

    def __init__(self, blob_client, src_url):
        self._dst_client = blob_client
        self._src_url = src_url
        self._src_client = BlobClient.from_blob_url(src_url)
        self._blob_size = self._src_client.get_blob_properties().size

    @property
    def blob_size(self):
        return self._blob_size

    @property
    def src_url(self):
        return self._src_url

    @property
    def target_task_size(self):
        # A copy task should be 4 MiB in size to use High-Throughput Block Blobs:
        # https://azure.microsoft.com/en-gb/blog/high-throughput-with-azure-blob-storage/
        # A copy task may not be more than 4 MiB.
        return 4 * 1024 * 1024

    @property
    def num_tasks(self):
        return math.ceil(self.blob_size / (self.target_task_size))

    def _create_blob(self):
        src_blob_properties = self._src_client.get_blob_properties()
        self._dst_client.create_page_blob(
            size=src_blob_properties.size,
            content_settings=src_blob_properties.content_settings,
            metadata=src_blob_properties.metadata
        )

    async def _copy_blob_contents(self):
        # We want to use async aio to chunk the PageBlob and copy the chunks concurrently.
        # For this we need to use the async blob client and create multiple tasks.
        # To limit the number of simultaneous dispatched network calls we use a semaphore.
        sem = asyncio.Semaphore(32)
        client = AioBlobClient.from_blob_url(self._dst_client.url, self._dst_client.credential.account_key)

        # The Aio Blob client throws errors when it is not properly closed.
        # Closing the credential and client helps:
        # https://github.com/Azure/azure-sdk-for-python/issues/16757
        #
        # This should be fixed when Azure Identity is updated to >=1.6:
        # https://github.com/Azure/azure-sdk-for-python/pull/9090
        async with client:
            tasks = [PageBlobCopier._copy_chunk(client, self._src_url, offset, size, sem)
                     for offset, size in self._get_copy_tasks()]

            previous_status = ""
            done_tasks = 0
            for task in asyncio.as_completed(tasks):
                await task
                done_tasks += 1
                progress = done_tasks / self.num_tasks * 100
                previous_status = report_progress(f"{datetime.now():%H:%M:%S}:     INFO: Copied: {progress:.2f}%",
                                                  previous_status)

            report_progress(f"{datetime.now():%H:%M:%S}:     INFO: Copied: 100.00%\n")

    @staticmethod
    @retry(
        reraise=True,
        retry=(retry_if_exception_type(HttpResponseError) | retry_if_exception_type(ServiceRequestError)),
        stop=stop_after_delay(300),
        wait=wait_random_exponential(multiplier=1, max=60),
    )
    async def _copy_chunk(async_client, src_url, offset, size, sem):
        async with sem:
            await async_client.upload_pages_from_url(src_url, offset, size, offset)

    def _get_copy_tasks(self):
        for chunk in range(self.num_tasks):
            offset = chunk * self.target_task_size
            if offset + self.target_task_size <= self.blob_size:
                yield offset, self.target_task_size
            else:
                chunk_size = self.blob_size - offset
                yield offset, chunk_size
