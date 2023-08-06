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

import clusterondemand.configuration
from clusterondemand.imagerepo import RepoImageSource, imagerepo_ns
from clusterondemand.imagetable import ALL_COLUMNS, make_cod_images_table
from clusterondemandconfig import ConfigNamespace, config

from .configuration import vmwarecommon_ns
from .images import findimages_ns

config_ns = ConfigNamespace("vmware.image.repolist", help_section="list output parameters")
config_ns.import_namespace(vmwarecommon_ns)
config_ns.import_namespace(findimages_ns)
config_ns.import_namespace(imagerepo_ns)
config_ns.import_namespace(clusterondemand.configuration.clusterlist_ns)
config_ns.add_enumeration_parameter(
    "sort",
    default=["created_at"],
    choices=[column[0] for column in ALL_COLUMNS],
    help="Sort results by one (or two) of the columns"
)
config_ns.add_enumeration_parameter(
    "columns",
    choices=[column[0] for column in ALL_COLUMNS],
    help="Provide space separated set of columns to be displayed"
)


def run_command():
    print(make_cod_images_table(
        RepoImageSource.find_images_using_options(config),
        sortby=config["sort"],
        advanced=config["advanced"],
        columns=config["columns"],
        output_format=config["output_format"]
    ))
