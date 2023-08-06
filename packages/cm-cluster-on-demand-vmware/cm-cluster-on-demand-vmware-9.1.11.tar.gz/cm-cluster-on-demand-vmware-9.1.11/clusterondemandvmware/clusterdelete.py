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

import clusterondemand
from clusterondemand.utils import generate_older_than_date, generate_timedelta, log_no_clusters_found
from clusterondemandconfig import ConfigNamespace, config
from clusterondemandvmware.network import network_ns
from clusterondemandvmware.ssh import remove_from_ssh_config

from . import clientutils
from .configuration import sshconfig_ns, vmwarecommon_ns
from .findclusters import VMWareClusterFinder, findclusters_ns

log = logging.getLogger("cluster-on-demand")


config_ns = ConfigNamespace("vmware.cluster.delete", help_section="cluster delete parameters")
config_ns.import_namespace(vmwarecommon_ns)
config_ns.import_namespace(clusterondemand.utils.confirm_ns)
config_ns.import_namespace(sshconfig_ns)
config_ns.import_namespace(findclusters_ns)
config_ns.import_namespace(network_ns)

config_ns.add_parameter(
    "older_than",
    parser=generate_timedelta,
    help=("Only remove clusters that are older than the specified time. "
          "It's possible to specify the amount of days/hours/minutes in the "
          "following form: '2d3h4m', '2d', '3d4h', '5h'")
)


def run_command():
    older_than_date = None

    def cluster_can_be_deleted(cluster):
        if older_than_date and cluster.get_creation_date() > older_than_date:
            log.warning(f"Cluster {cluster.name} won't be deleted because it's newer than the specified time")
            return False
        else:
            return True

    older_than_date = generate_older_than_date(config["older_than"])

    finder = VMWareClusterFinder()
    clusters, _ = finder.find_clusters_with_config()

    clusters = [
        c for c in clusters
        if cluster_can_be_deleted(c)
    ]

    if not clusters:
        log_no_clusters_found("delete")
        return

    clusters_to_delete = [cluster.name for cluster in clusters]
    log.info(f"""Will delete clusters: {", ".join(clusters_to_delete)}""")
    if not clusterondemand.utils.confirm():
        return

    clientutils.delete_clusters(clusters)
    if config["update_ssh_config"]:
        remove_from_ssh_config(config, clusters_to_delete)

    log.info("Done.")
