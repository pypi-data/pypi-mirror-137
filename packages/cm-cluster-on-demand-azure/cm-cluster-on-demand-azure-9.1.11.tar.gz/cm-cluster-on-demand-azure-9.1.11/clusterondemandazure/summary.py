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

from clusterondemand.summary import SummaryGenerator, SummaryType


class AzureSummaryGenerator(SummaryGenerator):
    """Generate the summary for creation of Azure clusters and nodes."""

    def __init__(self,
                 config,
                 summary_type,
                 region=None,
                 head_node_definition=None,
                 head_image=None,
                 instance_id=None,
                 node_definition=None,
                 public_ip=None):
        super().__init__(config["name"], region=region, config=config, summary_type=summary_type,
                         primary_head_node_definition=head_node_definition, head_image=head_image,
                         node_definitions=[node_definition])
        self._instance_id = instance_id
        self._public_ip = public_ip

    def _add_rows(self, table):
        if self._type == SummaryType.Proposal:
            self._add_resource_group(table)
            self._add_region(table)

        if self._type == SummaryType.Overview:
            self._add_deployment_details(table)

    def _add_deployment_details(self, table):
        table.add_row(["Head node ID:", self._instance_id])
        table.add_row(["Public IP:", self._public_ip])

    def _add_resource_group(self, table):
        table.add_row(["Resource Group:", self._config["resource_group"]])
