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
from collections import namedtuple

import pyVmomi

import clusterondemand.clustercreate
import clusterondemand.configuration
from clusterondemand.codoutput.sortingutils import SortableData
from clusterondemand.exceptions import CODException
from clusterondemand.utils import log_no_clusters_found
from clusterondemandconfig import ConfigNamespace, config

from . import clientutils
from .clientutils import get_server_cert_thumbprint
from .configuration import vmwarecommon_ns
from .findclusters import VMWareClusterFinder, findclusters_ns

log = logging.getLogger("cluster-on-demand")

COLUMN_HEADERS = {
    "cluster": "Cluster",
    "node": "Node",
    "hypervisor": "Hypervisor",
    "url": "WebUI URL"
}

ALL_COLUMNS = ["cluster", "node", "url"]
Row = namedtuple("Row", ALL_COLUMNS)

config_ns = ConfigNamespace("vmware.cluster.console", help_section="Cluster Console parameters")
config_ns.import_namespace(vmwarecommon_ns)
config_ns.import_namespace(clusterondemand.configuration.clusterlist_ns)
config_ns.import_namespace(findclusters_ns)
config_ns.override_imported_parameter("filters", default=["*"])
config_ns.add_enumeration_parameter(
    "columns",
    choices=ALL_COLUMNS,
    default=ALL_COLUMNS,
    help="Provide space separated set of columns to be displayed"
)


def run_command():
    log.info("Please wait...")

    finder = VMWareClusterFinder()
    all_clusters, _ = finder.find_clusters_with_config()
    if not all_clusters:
        log_no_clusters_found("console")
        return

    sm = clientutils.get_service_manager()

    # TODO: Make sure, that VSphere >= 7 supports generated URLs
    vsphere_major_version = int(sm.content.about.version.split(".")[0])
    if vsphere_major_version < 6:
        raise CODException("VSphere is too old to perform this operation")

    host = config["vmware_address"]
    guid = sm.content.about.instanceUuid
    ticket = sm.content.sessionManager.AcquireCloneTicket()
    thumbprint = get_server_cert_thumbprint(host, verify=config["vmware_verify_certificate"])

    # See https://github.com/noahfriedman/vmware-utils/blob/master/vspherelib.py (public domain)
    # This is a dumb thing to fault on, but overly restrictive
    # permissions might prevent us from inspecting vcenter to form a
    # preferred url.
    try:
        fqdn = next(s.value for s in sm.content.setting.setting if s.key == "VirtualCenter.FQDN")
    except pyVmomi.vmodl.fault.SecurityError:
        log.warning("Failed to get server's FQDN, using hostname...")
        fqdn = None
    # Might be None for an esxi session
    if not fqdn:
        fqdn = host

    log.info(f"Please note that you still need to log in to the https://{host}/ui/"
             f" before using the console URLs")
    table_rows = []
    for cluster in all_clusters:
        for vm in cluster.get_vms():
            if vm.runtime.powerState != "poweredOn":
                log.warning(f"Cannot get URL for '{vm.name}': power state is {vm.runtime.powerState}")
                continue
            console_url = (
                f"https://{host}/ui/webconsole.html"
                f"?vmId={vm._GetMoId()}"
                f"&vmName={vm.name}"
                f"&serverGuid={guid}"
                f"&host={fqdn}"
                f"&sessionTicket={ticket}"
                f"&thumbprint={thumbprint}"
            )
            cluster_name = cluster.name
            node_name = vm.name
            table_rows.append(Row(cluster_name, node_name, console_url))

    table_rows.sort(key=lambda row: (row.cluster, row.node))
    columns = config["columns"]
    col_headers = [(col, COLUMN_HEADERS[col]) for col in columns]
    rows = [[getattr(row, column) for column in columns] for row in table_rows]

    table = SortableData(
        all_headers=col_headers,
        requested_headers=columns,
        rows=rows,
    )
    table.sort()
    print(table.output(config["output_format"]))
