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

from clusterondemandazure.azure_actions.storage import StorageAction

from .vmsizelist import VMSizesList


class AZUREParamValidator(object):

    @staticmethod
    def validate_location(azure_api, location):
        return VMSizesList.is_valid_location(azure_api, location)

    @staticmethod
    def validate_vmsize(azure_api, location, vmsize_name):
        vmsizes = []
        paged_vmsizes = azure_api.compute_client.virtual_machine_sizes.list(location=location)
        next_page = next(paged_vmsizes)
        while next_page:
            if not isinstance(next_page, list):
                next_page = [next_page]
            for vmsize in next_page:
                vmsizes.append(vmsize.name.lower())
            try:
                next_page = next(paged_vmsizes)
            except (GeneratorExit, StopIteration):
                break
        return vmsize_name.lower() in vmsizes

    @staticmethod
    def validate_custom_blob(blob_url):
        try:
            StorageAction.get_blob_metadata(blob_url)
        except Exception:
            return False
        return True

    @staticmethod
    def validate_password(password):
        return len(password) >= 8
