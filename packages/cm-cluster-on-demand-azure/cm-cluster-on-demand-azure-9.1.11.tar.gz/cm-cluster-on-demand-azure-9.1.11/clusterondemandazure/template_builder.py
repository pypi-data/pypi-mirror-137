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

import json
import logging
import os

from clusterondemandconfig import config

log = logging.getLogger("cluster-on-demand")


class TemplateBuilder(object):

    def __init__(self, head_node_name, head_node_flavour, storage_account,
                 region, user_random_password, custom_data, head_node_ip, network_cidr, subnet_cidr,
                 head_node_root_volume_size, head_node_root_volume_type,
                 image_name, image_creation_date, inbound_rules):

        # TODO Use the parameters instead of doing a string replacement
        self.keys = {
            "${head_node_name}": head_node_name,
            "${head_node_flavour}": head_node_flavour,
            "${storage_account_name}": storage_account,
            "${region}": region,
            "${user_random_password}": user_random_password,
            "${custom_data}": custom_data,
            "${network_cidr}": network_cidr,
            "${subnet_cidr}": subnet_cidr,
            "${head_node_ip}": head_node_ip,
            "${head_node_root_volume_size}": str(head_node_root_volume_size),
            "${head_node_root_volume_type}": head_node_root_volume_type,
            "${image_name}": image_name,
            "${image_creation_date}": image_creation_date,
            "${inbound_rules}": inbound_rules
        }

    def fill_template(self, template):
        for place_holder, value in self.keys.items():
            if value and isinstance(value, str):
                template = template.replace(place_holder, value)
        return template

    def get_resource(self, type):
        template = open(os.path.join(os.path.dirname(__file__), "resources/%s.json") % type)
        return json.load(template)

    def get_head_node_resource(self):
        return self.get_resource("head-node")

    def get_head_node_nic_resource(self):
        nic_resource = self.get_resource("head-node-nic")
        if not config["create_public_ip"]:
            # TODO CM-28902 should handle this in a better way. It's a bit annoying to modify the templates (why have
            # them in separate files if we modify?)
            # Once it's unified in a single template.json, then I think one way of achieving would be to define two
            # sorts of "head-node-nic" and they are deployed conditionally depending on parameter "create_public_ip"
            del nic_resource["properties"]["ipConfigurations"][0]["properties"]["publicIPAddress"]
        return nic_resource

    def get_pub_ip_resource(self):
        return self.get_resource("pub-ip")

    def get_sec_group_resource(self):
        return self.get_resource("sec-group")

    def get_vpc_resource(self):
        return self.get_resource("vpc")

    def get_avset_resource(self):
        return self.get_resource("avset")

    def build(self):
        template = open(os.path.join(os.path.dirname(__file__), "template.json")).read()
        template = json.loads(self.fill_template(template))

        # TODO (CM-28902): Move everything to inside template.json then we don't need this
        template["resources"].append(self.get_head_node_resource())
        template["resources"].append(self.get_head_node_nic_resource())
        template["resources"].append(self.get_pub_ip_resource())
        template["resources"].append(self.get_sec_group_resource())
        template["resources"].append(self.get_vpc_resource())
        template["resources"].append(self.get_avset_resource())

        return template
