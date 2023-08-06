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

from __future__ import absolute_import, print_function

import logging

import clusterondemand.clustercreate
import clusterondemand.configuration
from clusterondemand import const
from clusterondemand.codoutput.sortingutils import SortableData, SSHAlias
from clusterondemand.ssh import MultipleCodTypesException
from clusterondemand.tags import get_packagegroups_from_tags, parse_cluster_tags
from clusterondemand.utils import format_to_local_date_time, get_time_ago_from_iso, log_no_clusters_found
from clusterondemandconfig import ConfigNamespace, config
from clusterondemandvmware.ssh import VMwareSSHConfigManager

from .configuration import sshconfig_ns, vmwarecommon_ns
from .findclusters import VMWareClusterFinder, findclusters_ns

log = logging.getLogger("cluster-on-demand")

ALL_COLUMNS = {
    "index": "Index",
    "ssh": "SSH",
    "name": "Cluster Name",
    "head_status": "Head status",
    "ip": "IP",
    "created": "Created (age)",
    "vlan_id": "VLAN ID",
    "head_image_name": "Head image",
    "head_image_age": "Image age",
    "cmd_revision": "CMD rev.",
    "distro": "Distro",
    "version": "Version",
    "packages": "Packages",
    "head_image_rev": "Image rev.",
    "head_image_created": "Image created",
    "internalnet_network_backend": "Internalnet backend",
    "externalnet_network_backend": "Externalnet backend",
}

DEFAULT_COLUMNS = [
    "name",
    "ip",
    "created",
    "head_status",
    "head_image_name",
    "head_image_age",
    "vlan_id",
]

assert all(col in ALL_COLUMNS for col in DEFAULT_COLUMNS)

config_ns = ConfigNamespace("vmware.cluster.list", "list output parameters")
config_ns.import_namespace(vmwarecommon_ns)
config_ns.import_namespace(clusterondemand.configuration.clusterlist_ns)
config_ns.import_namespace(findclusters_ns)
config_ns.import_namespace(sshconfig_ns)
config_ns.override_imported_parameter("filters", default=["*"])
config_ns.add_enumeration_parameter(
    "sort",
    default=["created"],
    choices=list(ALL_COLUMNS.keys()),
    help="Sort results by one (or two) of the columns"
)
config_ns.add_enumeration_parameter(
    "columns",
    choices=list(ALL_COLUMNS.keys()),
    default=DEFAULT_COLUMNS,
    help="Provide space separated set of columns to be displayed"
)


def run_command():
    log.info("Listing clusters...")

    # We have to preserve the order from config["columns"] in requested_columns
    requested_columns = [(col, ALL_COLUMNS[col]) for col in config["columns"]]

    finder = VMWareClusterFinder()
    clusters, _ = finder.find_clusters_with_config()

    with VMwareSSHConfigManager.lock():
        try:
            # We should only parse the ssh config if we are updating it or need to extract some information.
            parse = config["update_ssh_config"] or any(column[0] in ["ssh", "index"] for column in requested_columns)
            mode = "replace-hosts" if config["update_ssh_config"] else "match-hosts"
            ssh_manager = VMwareSSHConfigManager(mode=mode, parse=parse, prefix=config["ssh_config_alias_prefix"])
        except MultipleCodTypesException:
            message = ("Cannot parse SSH config files containing multiple COD types. To update "
                       "the SSH config with the current clusters add an SSH prefix by setting "
                       "--ssh-config-alias-prefix or adding ssh_config_alias_prefix to the "
                       "config and running 'cm-cod-vmware cluster list --update-ssh-config'.")
            log.warning(message)
            ssh_manager = None

        rows = []
        for cluster in clusters:
            if ssh_manager and config["update_ssh_config"]:
                try:
                    external_ip = cluster.get_head_node_external_ipv4()
                except Exception:
                    log.debug(f"No external IP found for {cluster.name}, probably it's stopped")
                else:
                    ssh_manager.add_host(cluster.name, external_ip)
            row = get_cluster_info(cluster, requested_columns, ssh_manager)
            rows.append(row)

        if ssh_manager and config["update_ssh_config"]:
            ssh_manager.write_configuration()

    if rows:
        table = SortableData(all_headers=requested_columns, requested_headers=config["columns"], rows=rows)
        table.sort(*config["sort"])
        print(table.output(output_format=config["output_format"]))
    else:
        log_no_clusters_found("list")


def get_cluster_info(cluster, requested_columns, ssh_manager):
    tags = cluster.get_tags()
    tags_dict, _ = parse_cluster_tags(tags)
    cluster_info = []
    for column, _ in requested_columns:
        if column == "name":
            cluster_info.append(cluster.name)
        elif column == "head_status":
            head_vm = cluster.get_head_node()
            cluster_info.append(head_vm.summary.runtime.powerState if head_vm is not None else "?")
        elif column == "ip":
            try:
                cluster_info.append(cluster.get_head_node_external_ipv4())
            except Exception:
                cluster_info.append("?")
        elif column == "vlan_id":
            vlan_id = cluster.get_vlan_id()
            cluster_info.append(vlan_id)
        elif column == "distro":
            cluster_info.append(tags_dict.get(const.COD_DISTRO_TAG, "?"))
        elif column == "version":
            cluster_info.append(tags_dict.get(const.COD_VERSION_TAG, "?"))
        elif column == "head_image_name":
            cluster_info.append(tags_dict.get(const.COD_HEAD_IMAGE_NAME, "?"))
        elif column == "cmd_revision":
            cluster_info.append(tags_dict.get(const.COD_CMDREV_TAG, "?"))
        elif column == "head_image_rev":
            cluster_info.append(tags_dict.get(const.COD_HEAD_IMAGE_REV, "?"))
        elif column == "packages":
            cluster_info.append(",".join(sorted(get_packagegroups_from_tags(tags))))
        elif column == "head_image_age":
            try:
                image_date = tags_dict.get(const.COD_HEAD_IMAGE_CREATED_AT)
                cluster_info.append(get_time_ago_from_iso(image_date) if image_date else "?")
            except Exception as e:
                log.debug(f"Cannot determine image age: {e}")
                cluster_info.append("?")
        elif column == "head_image_created":
            try:
                image_date = tags_dict.get(const.COD_HEAD_IMAGE_CREATED_AT)
                cluster_info.append(format_to_local_date_time(image_date) if image_date else "?")
            except Exception as e:
                log.debug(f"Cannot determine image creation date: {e}")
                cluster_info.append("?")
        elif column == "index":
            try:
                index = ssh_manager.get_host_index(cluster.name)
                cluster_info.append(index)
            except Exception as e:
                log.debug(f"Cannot determine cluster index: {e}")
                cluster_info.append("?")
        elif column == "ssh":
            try:
                alias = ssh_manager.get_host_alias(cluster.name)
                cluster_info.append(alias)
            except Exception as e:
                log.debug(f"Cannot determine cluster index: {e}")
                cluster_info.append(SSHAlias("?"))
        elif column == "created":
            cluster_info.append(cluster.get_creation_date())
        elif column == "internalnet_network_backend":
            cluster_info.append(cluster.get_internalnet_network_backend())
        elif column == "externalnet_network_backend":
            try:
                cluster_info.append(cluster.get_externalnet_network_backend())
            except Exception as e:
                log.debug(f"Cannot determine externalnet network backend: {e}")
                cluster_info.append("?")

    return cluster_info
