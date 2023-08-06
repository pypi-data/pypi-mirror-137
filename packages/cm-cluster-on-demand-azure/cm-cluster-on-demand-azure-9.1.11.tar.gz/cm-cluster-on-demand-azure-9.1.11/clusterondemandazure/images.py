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
import re

from azure.storage.blob import ContainerClient

from clusterondemand.exceptions import CODException
from clusterondemand.images.find import CODImage, ImageSource
from clusterondemand.images.find import findimages_ns as common_findimages_ns
from clusterondemandconfig import ConfigNamespace, config

from .azure_actions.throttle import unt

log = logging.getLogger("cluster-on-demand")


def must_be_valid_container_url(parameter, configuration):
    """Validation that raises an error when the container url does not match the proper format"""
    container_urls = configuration[parameter.key]
    for container_url in container_urls:
        if not re.match(CONTAINER_URL_REGEX, container_url):
            raise CODException("Invalid image container URI: %s; must match: %s" % (container_url, CONTAINER_URL_REGEX))


findimages_ns = ConfigNamespace("azure.images.find", help_section="image filter parameters")
findimages_ns.import_namespace(common_findimages_ns)
findimages_ns.override_imported_parameter("cloud_type", default="azure")
findimages_ns.add_enumeration_parameter(
    "container_url",
    default=["https://brightimages.blob.core.windows.net/images/"],
    help="One or several azure container urls to list images from",
    validation=must_be_valid_container_url
)

IMAGE_NAME_REGEX_AZURE = r"^((?:bcm-cod-image-)([^-]+(?:-dev)?)(?:-([^-]+))?-(.*)).vhd$"
CONTAINER_URL_REGEX = r"(http|https)://(?P<storage_account>[^\.]+).blob.core.windows.net/(?P<container>.+)"


class CannotParseImageName(Exception):
    pass


class AzureImageSource(ImageSource):
    @classmethod
    def from_config(cls, config, ids=None):
        return AzureImageSource(
            ids=ids if ids is not None else config["ids"],
            version=config["version"],
            distro=config["distro"],
            status=config["status"],
            advanced=True,
            image_visibility=config["image_visibility"],
            cloud_type=config["cloud_type"],
        )

    def _iter_from_source(self):
        for url in config["container_url"]:
            container_client = ContainerClient.from_container_url(url)
            for blob in unt(container_client.list_blobs):
                try:
                    cod_image = make_cod_image_from_azure(blob, url)
                except CannotParseImageName as e:
                    # This is parsing names of public images, someone could even upload some bogus name
                    # to break our code. So we just ignore if we can't parse it
                    # Other exception can blow up
                    log.debug(e)
                else:
                    yield cod_image


def make_cod_image_from_azure(blob, container_url):
    match = re.match(IMAGE_NAME_REGEX_AZURE, blob.name)
    if not match:
        raise CannotParseImageName(f"Cannot parse image name {blob.name}")

    name, version, distribution, revision = match.groups()

    # Prior to CM-35092, we didn't have the distro in the image name
    # So some of them don't have it.
    # We just set as "centos" without specifying version
    if not distribution:
        distribution = "centos"

    return CODImage(
        name=name,
        id=f"{distribution}-{version}",
        uuid=container_url + blob.name,
        revision=int(revision),
        version=version,
        distro=distribution if distribution else "",
        size=blob.size,
        created_at=blob.creation_time,
        image_visibility="N/A",
        type="headnode",
        cloud_type="azure",
    )
