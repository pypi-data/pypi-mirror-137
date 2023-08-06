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

from clusterondemand.ssh import MultipleCodTypesException, SSHConfigManager

log = logging.getLogger("cluster-on-demand")


class VMwareSSHConfigManager(SSHConfigManager):

    """
    A helper class to manage cluster-related entries in local ssh_config file.

    :param ssh_config: the path of the local ssh configuration file to use.
    :param prefix: the prefix used to build the cluster ssh aliases.
    :param parse: enable parsing the contents of the ssh_config file.
    :param mode: Either "match-hosts" or "replace-hosts". "match-hosts" preserves the contents of the
                 COD section or the ssh_config file; "replace-hosts" ignores currently defined hosts.
                 User-defined contents are always preserved.
    """
    def __init__(self, ssh_config="~/.ssh/config", prefix="", parse=True, mode="match-hosts"):
        super().__init__("vmware", ssh_config, prefix, parse, mode)


def add_to_ssh_config(config, cluster_name, floating_ip):
    with VMwareSSHConfigManager.lock():
        try:
            ssh_manager = VMwareSSHConfigManager(parse=config["update_ssh_config"],
                                                 prefix=config["ssh_config_alias_prefix"])
        except MultipleCodTypesException:
            message = ("Cannot parse SSH config files containing multiple COD types. As a result the cluster will "
                       "not be added the SSH config. To add the cluster to the SSH config set an SSH prefix by "
                       "setting --ssh-config-alias-prefix or adding ssh_config_alias_prefix to the config and running "
                       "cm-cod-vmware cluster list --update-ssh-config.")
            log.warning(message)
            return f"ssh root@{floating_ip}"

        host_descriptor = ssh_manager.add_host(cluster_name, floating_ip, override=True)
        ssh_manager.write_configuration()
        connection_string = f"ssh {host_descriptor.alias} (alias defined in ~/.ssh/config)"

        return connection_string


def remove_from_ssh_config(config, clusters):
    with VMwareSSHConfigManager.lock():
        try:
            ssh_manager = VMwareSSHConfigManager(parse=True,
                                                 prefix=config["ssh_config_alias_prefix"])
        except MultipleCodTypesException:
            message = ("Cannot parse SSH config files containing multiple COD types. As a result the cluster "
                       "is not removed from the SSH config. To remove the cluster from the SSH config set an SSH "
                       "prefix by setting --ssh-config-alias-prefix or adding ssh_config_alias_prefix to the config "
                       "and running cm-cod-vmware cluster list --update-ssh-config.")
            log.warning(message)
            return

        for cluster in clusters:
            ssh_manager.remove_host(cluster)

        ssh_manager.write_configuration()


def update_in_ssh_config(config, cluster_ips):
    with VMwareSSHConfigManager.lock():
        try:
            ssh_manager = VMwareSSHConfigManager(parse=True,
                                                 prefix=config["ssh_config_alias_prefix"])
        except MultipleCodTypesException:
            message = ("Cannot parse SSH config files containing multiple COD types. As a result the cluster "
                       "is not updated in SSH config. To update the cluster in the SSH config set an SSH "
                       "prefix by setting --ssh-config-alias-prefix or adding ssh_config_alias_prefix to the config "
                       "and running cm-cod-vmware cluster list --update-ssh-config.")
            log.warning(message)
            return

        for cluster_name, external_ip in cluster_ips.items():
            try:
                ssh_manager.remove_host(cluster_name)
            except Exception:
                pass

            ssh_manager.add_host(cluster_name, external_ip)

        ssh_manager.write_configuration()
