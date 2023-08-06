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

from prettytable import PrettyTable

from clusterondemand.utils import log_no_clusters_found
from clusterondemandconfig import ConfigNamespace
from clusterondemandvmware.clientutils import get_network_id
from clusterondemandvmware.configuration import vmwarecommon_ns
from clusterondemandvmware.findclusters import VMWareClusterFinder, findclusters_ns
from clusterondemandvmware.network import NetworkBackend

log = logging.getLogger("cluster-on-demand")

config_ns = ConfigNamespace("vmware.cluster.show", "cluster show parameters")
config_ns.import_namespace(vmwarecommon_ns)
config_ns.import_namespace(findclusters_ns)


def run_command():
    clusters = _get_clusters()

    for cluster in clusters:
        _show_cluster(cluster)


def _get_clusters():
    finder = VMWareClusterFinder()
    clusters, _ = finder.find_clusters_with_config()

    if not clusters:
        log_no_clusters_found("show")

    return clusters


def _show_cluster(cluster):
    field_names = ["Type", "Name", "Id", "Status", "Power"]
    table = PrettyTable(field_names)
    table.align = "l"
    table.sortby = "Type"

    _add_network_to_table(cluster, table, field_names)
    _add_vms_to_table(cluster, table, field_names)

    print(table)


def _add_network_to_table(cluster, table, field_names):
    backend = cluster.get_internalnet_network_backend()
    if backend == NetworkBackend.VSPHERE:
        network_type = "Distributed Virtual Portgroup"
    elif backend == NetworkBackend.NSX:
        network_type = "NSX Logical Switch"
    else:
        raise NotImplementedError(f"Show cluster is not implement for network type {backend}")

    network_info = {
        "Name": cluster.internal_net.name,
        "Type": network_type,
        "status": cluster.internal_net.overallStatus,
        "Id": get_network_id(cluster.internal_net.name)
    }

    line = _create_line(field_names, network_info)
    table.add_row(line)


def _add_vms_to_table(cluster, table, field_names):
    for vm in cluster.get_vms():
        vm_info = {
            "Type": "Virtual Machine",
            "Name": vm.name,
            "Power": _get_power_state(vm.runtime.powerState),
            "Status": vm.overallStatus,
            "Id": re.search("vm-[0-9]+", str(vm)).group()
        }

        line = _create_line(field_names, vm_info)
        table.add_row(line)


def _create_line(field_names, item):
    return [item.get(field, "") for field in field_names]


def _get_power_state(power_state):
    state_mapping = {
        "poweredOn": "On",
        "suspended": "Suspended",
        "poweredOff": "Off"
    }

    return state_mapping.get(power_state)
