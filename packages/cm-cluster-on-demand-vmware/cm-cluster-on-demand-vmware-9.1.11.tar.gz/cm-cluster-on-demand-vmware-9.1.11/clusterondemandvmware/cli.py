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

import clusterondemand.configuration
import clusterondemandconfig
from clusterondemand.command_runner import run_invoked_command

from . import (
    clusterconsole,
    clustercreate,
    clusterdelete,
    clusterlist,
    clustershow,
    clusterstart,
    clusterstop,
    configdump,
    configshow,
    configuration,
    imagedelete,
    imageinstall,
    imagelist,
    imagerepolist,
    imagetag
)

log = logging.getLogger("cluster-on-demand")


vmware_commands = clusterondemandconfig.CommandContext("cm-cod-vmware")
vmware_commands.add_group("cm-cod-vmware cluster", "Manage clusters", aliases=["c"])
vmware_commands.add_command(
    "cm-cod-vmware cluster create",
    clustercreate,
    "Create a new cluster",
    aliases=["c"],
    important_help_sections=[
        clustercreate.config_ns,
        clusterondemand.configuration.clustercreatepassword_ns,
        clusterondemand.configuration.clustercreatelicense_ns,
        configuration.vmwarecredentials_ns
    ]
)
vmware_commands.add_command(
    "cm-cod-vmware cluster delete",
    clusterdelete,
    "Delete clusters",
    aliases=["d"],
    important_help_sections=[
        clusterlist.config_ns,
        clusterondemand.configuration.clusterprefix_ns
    ]
)
vmware_commands.add_command(
    "cm-cod-vmware cluster list",
    clusterlist,
    "List clusters",
    aliases=["l"],
    important_help_sections=[
        clusterlist.config_ns,
        clusterondemand.configuration.clusterprefix_ns
    ]
)
vmware_commands.add_command(
    "cm-cod-vmware cluster show",
    clustershow,
    "Show clusters",
    aliases=["s"],
    important_help_sections=[
        clusterlist.config_ns,
        clusterondemand.configuration.clusterprefix_ns
    ]
)
vmware_commands.add_command(
    "cm-cod-vmware cluster console",
    clusterconsole,
    "Get web-based console URLs for cluster nodes of specified clusters.",
    important_help_sections=[
        clusterconsole.config_ns,
        clusterondemand.configuration.clusterprefix_ns
    ]
)
vmware_commands.add_command(
    "cm-cod-vmware cluster start",
    clusterstart,
    "Start the head node instances for clusters",
    important_help_sections=[
        clusterstart.config_ns,
        clusterondemand.configuration.clusterprefix_ns,
    ]
)
vmware_commands.add_command(
    "cm-cod-vmware cluster stop",
    clusterstop,
    "Stop all instances for clusters",
    important_help_sections=[
        clusterstop.config_ns,
        clusterondemand.configuration.clusterprefix_ns,
    ]
)

vmware_commands.add_group("cm-cod-vmware image", "Manage images", aliases=["i"])
vmware_commands.add_command(
    "cm-cod-vmware image list",
    imagelist,
    "List images",
    aliases=["l"],
    important_help_sections=[
        imagelist.config_ns,
    ]
)
vmware_commands.add_command(
    "cm-cod-vmware image repo-list",
    imagerepolist,
    "Lists images in the repository",
    important_help_sections=[
        imagerepolist.config_ns,
    ]
)
vmware_commands.add_command(
    "cm-cod-vmware image install",
    imageinstall,
    "Create image in the content library",
    important_help_sections=[
        imageinstall.config_ns
    ]
)
vmware_commands.add_command(
    "cm-cod-vmware image delete",
    imagedelete,
    "Delete images from the content library",
    important_help_sections=[
        imagedelete.config_ns
    ]
)
vmware_commands.add_command(
    "cm-cod-vmware image tag",
    imagetag,
    "Modify tags of specified image(s)",
    important_help_sections=[
        imagetag.config_ns
    ]
)
vmware_commands.add_group("cm-cod-vmware config", "Configuration operations")
vmware_commands.add_command(
    "cm-cod-vmware config dump",
    configdump,
    configdump.COMMAND_HELP_TEXT,
    require_eula=False
)
vmware_commands.add_command(
    "cm-cod-vmware config show",
    configshow,
    configshow.COMMAND_HELP_TEXT,
    require_eula=False
)


def cli_main():
    run_invoked_command(vmware_commands)
