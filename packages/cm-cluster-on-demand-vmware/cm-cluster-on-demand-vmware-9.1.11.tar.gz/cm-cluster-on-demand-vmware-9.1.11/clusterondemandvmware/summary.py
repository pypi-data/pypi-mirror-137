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

from clusterondemand.summary import SummaryGenerator


class VmwareSummaryGenerator(SummaryGenerator):
    """Generate the summary for creation of VMware clusters and nodes."""

    def __init__(self,
                 head_name,
                 summary_type,
                 config=None,
                 head_node_definition=None,
                 head_image=None,
                 node_definition=None,
                 node_image=None,
                 ssh_string=None,
                 ip=None):

        super().__init__(head_name,
                         config=config,
                         primary_head_node_definition=head_node_definition,
                         head_image=head_image,
                         ip=ip,
                         node_definitions=[node_definition],
                         node_image=node_image,
                         ssh_string=ssh_string,
                         summary_type=summary_type)
