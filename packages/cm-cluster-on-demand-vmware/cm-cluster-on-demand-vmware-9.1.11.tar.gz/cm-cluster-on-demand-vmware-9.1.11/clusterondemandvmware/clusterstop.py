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
import time

from clusterondemand.cmclient import CMDaemonJSONClient
from clusterondemand.ssh import SSHExecutor, clusterssh_ns
from clusterondemand.utils import MultithreadRunError, confirm, confirm_ns, log_no_clusters_found, multithread_run
from clusterondemandconfig import ConfigNamespace, config
from clusterondemandvmware.ssh import remove_from_ssh_config

from . import clientutils
from .configuration import sshconfig_ns, vmwarecommon_ns
from .findclusters import VMWareClusterFinder, findclusters_ns

log = logging.getLogger("cluster-on-demand")


config_ns = ConfigNamespace("vmware.cluster.stop", help_section="cluster stop parameters")
config_ns.import_namespace(vmwarecommon_ns)
config_ns.import_namespace(sshconfig_ns)
config_ns.import_namespace(findclusters_ns)
config_ns.import_namespace(confirm_ns)
config_ns.import_namespace(clusterssh_ns)


def run_command():
    finder = VMWareClusterFinder()
    clusters, _ = finder.find_clusters_with_config()
    if not clusters:
        log_no_clusters_found("stop")
        return

    active_clusters = [c for c in clusters if c.get_head_node().runtime.powerState == "poweredOn"]
    if not active_clusters:
        log.info("No powered on clusters found")
        return

    # Gracefully shut down clusters.
    log.info("Stopping clusters: %s", ", ".join([c.name for c in active_clusters]))
    if not confirm():
        return

    results = multithread_run(_stop_cluster, active_clusters, max_threads=5)

    stopped_cluster_names = []
    for cluster, result in zip(active_clusters, results):
        if isinstance(result, MultithreadRunError):
            log.error(f"Failed to stop cluster '{cluster.name}': {result.exception}")
            log.debug(result.traceback)
        else:  # succeeded
            stopped_cluster_names.append(cluster.name)

    # Just in case, power off any remaining clusters' VMs. This should not be really needed.
    _power_off_clusters_vms(active_clusters)

    if config["update_ssh_config"]:
        log.debug(f"Updating ssh config")
        remove_from_ssh_config(config, stopped_cluster_names)

    log.info("Done")


def _stop_cluster(cluster):
    external_ip = cluster.get_head_node_external_ipv4()
    cmclient = CMDaemonJSONClient(external_ip)
    compute_nodes = cmclient.getComputeNodes()
    head_vm = cluster.get_head_node()

    # Shut down compute nodes.
    if compute_nodes:
        log.info(f"{cluster.name}: Shutting down compute nodes via CMDaemon API")
        cmclient.pshutdown([node["uniqueKey"] for node in compute_nodes])
        compute_nodes_vms = [vm for vm in cluster.get_vms() if vm != head_vm]
        _wait_for_vms_to_poweroff(cluster, compute_nodes_vms)
    else:
        log.info("No compute nodes to be shut down")

    # Shut down head node.
    log.info(f"{cluster.name}: Shutting down head node")
    SSHExecutor(external_ip, raise_exceptions=False).call("shutdown now")
    _wait_for_vms_to_poweroff(cluster, [head_vm])


def _wait_for_vms_to_poweroff(cluster, vms):
    log.debug(f"{cluster.name}: Waiting for nodes to shut down: %s", ", ".join([vm.name for vm in vms]))
    active_vms = vms

    while True:
        log.debug(f"{cluster.name}: Power states: %s",
                  ", ".join([f"{vm.name}: {vm.runtime.powerState}" for vm in vms]))
        active_vms = [vm for vm in vms if vm.runtime.powerState == "poweredOn"]
        if not active_vms:
            break
        time.sleep(5)


def _power_off_clusters_vms(clusters):
    vms = [vm for c in clusters for vm in c.get_vms()]
    active_vms = [vm for vm in vms if vm.runtime.powerState == "poweredOn"]
    if active_vms:
        log.warning("Powering off VMs that somehow failed to shut down: %s", ", ".join(vm.name for vm in active_vms))
        clientutils.power_off_vms(active_vms)
    else:
        log.debug("No more running VMs found, as expected")
