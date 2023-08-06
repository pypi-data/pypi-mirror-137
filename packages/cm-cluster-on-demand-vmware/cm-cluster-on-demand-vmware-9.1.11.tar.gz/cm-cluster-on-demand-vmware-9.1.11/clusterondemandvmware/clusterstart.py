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

import concurrent.futures
import logging

from clusterondemand.ssh import clusterssh_ns
from clusterondemand.utils import confirm, confirm_ns, log_no_clusters_found
from clusterondemandconfig import ConfigNamespace, config
from clusterondemandvmware.ssh import update_in_ssh_config

from . import clientutils
from .configuration import sshconfig_ns, vmwarecommon_ns
from .findclusters import VMWareClusterFinder, findclusters_ns

log = logging.getLogger("cluster-on-demand")

config_ns = ConfigNamespace("vmware.cluster.start", help_section="cluster start parameters")
config_ns.import_namespace(vmwarecommon_ns)
config_ns.import_namespace(sshconfig_ns)
config_ns.import_namespace(findclusters_ns)
config_ns.import_namespace(confirm_ns)
config_ns.import_namespace(clusterssh_ns)


def run_command():
    finder = VMWareClusterFinder()
    clusters, _ = finder.find_clusters_with_config()
    if not clusters:
        log_no_clusters_found("start")
        return

    inactive_clusters = [c for c in clusters if c.get_head_node().runtime.powerState != "poweredOn"]
    if not inactive_clusters:
        log.info("No powered off clusters found")
        return

    # Power on head nodes.
    log.info("Starting clusters: %s", ", ".join(c.name for c in inactive_clusters))
    if not confirm():
        return

    plural = "s" if len(inactive_clusters) > 1 else ""
    inactive_head_vms = [c.get_head_node() for c in inactive_clusters]
    log.info(f"Powering on VM{plural}: %s", ", ".join(vm.name for vm in inactive_head_vms))
    clientutils.power_on_vms(inactive_head_vms)
    log.info(f"Powered on head node VM{plural}, awaiting new external IP{plural}")
    cluster_ips = _get_external_ips(inactive_clusters)
    for head_vm in inactive_head_vms:
        external_ip = cluster_ips.get(head_vm.name)
        clientutils.unmount_ovf_environment_image(head_vm, external_ip)

    if config["update_ssh_config"]:
        log.debug(f"Updating ssh config with new external IP{plural}")
        update_in_ssh_config(config, cluster_ips)

    log.info("Done")


def _get_external_ips(clusters):
    cluster_ips = {}
    head_nodes = [cluster.get_head_node() for cluster in clusters]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        get_ip_for_vm = {
            executor.submit(clientutils.get_headnode_external_ip, head_vm, wait=True): head_vm for head_vm in head_nodes
        }

        for future in concurrent.futures.as_completed(get_ip_for_vm):
            try:
                external_ip = future.result()
                head_vm = get_ip_for_vm[future]
                log.debug(f"Cluster {head_vm.name} IP: {external_ip}")
                cluster_ips[head_vm.name] = external_ip
            except Exception as e:
                log.error(e)
                next

    return cluster_ips
