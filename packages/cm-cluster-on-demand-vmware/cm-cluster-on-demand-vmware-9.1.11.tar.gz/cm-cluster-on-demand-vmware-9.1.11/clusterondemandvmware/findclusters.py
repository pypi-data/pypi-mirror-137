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

from __future__ import absolute_import

import logging

from clusterondemand.exceptions import CODException
from clusterondemand.findclusters import ClusterFinder
from clusterondemand.findclusters import findclusters_ns as common_findclusters_ns
from clusterondemandconfig import ConfigNamespace
from clusterondemandvmware.network import NetworkBackend

from . import clientutils

log = logging.getLogger("cluster-on-demand")


class VMwareCluster:
    """Class to encapsulate a VMWare cluster

    A cluster contains, at the minimum, a VirtualMachine for the head node and a Network for the internal net

    The head node VM holds the tags about the cluster and is considered the "main" part, the rest is derived
    from it.

    Every cluster will be attached to 2 networks. By definition, the head node vm and and the internal network
    have the <cluster name> as their name

    The nodes of the cluster are all VMs attached to the internal network.

    The external network, by definition, will be the networks that is not the internal network.
    """
    name = None
    head_vm = None
    internal_net = None

    def __init__(self, head_vm):
        self.name = head_vm.name
        self.head_vm = head_vm
        self.internal_net = clientutils.get_network(self.name)

    def get_head_node_name(self):
        return self.name

    def get_head_node(self):
        try:
            hn_name = self.get_head_node_name()
            head_vm = next(vm for vm in self.internal_net.vm if vm.name == hn_name)
        except StopIteration:
            raise Exception(f"Cannot find head node in cluster {self.name}")

        return head_vm

    def get_head_node_external_ipv4(self):
        return clientutils.get_headnode_external_ip(self.head_vm)

    def get_vms(self):
        return self.internal_net.vm

    def get_vlan_id(self):
        # The VLAN ID can only be retrieved on vSphere managed networks.
        # This means that in case of a non vSphere managed network we can't display the VLAN.
        if self.get_internalnet_network_backend() == NetworkBackend.VSPHERE:
            return self.internal_net.config.defaultPortConfig.vlan.vlanId
        else:
            return "N/A"

    def get_internalnet_network_backend(self):
        return NetworkBackend.get_backend_for_network(self.internal_net)

    def get_externalnet_network_backend(self):
        # Headnodes have two nics. We connect nic0 to the internal net and nic1 to the external net.
        network_name = self.head_vm.guest.net[1].network
        # The networks attached to the VM only have a name if the network is backed by vSphere.
        # This means that (for now) we can assume an NSX based network if the network has no name.
        if network_name:
            return NetworkBackend.VSPHERE
        else:
            return NetworkBackend.NSX

    def get_tags(self):
        return clientutils.get_service_manager().get_tags(self.head_vm)

    def get_creation_date(self):
        return self.head_vm.config.createDate


class VMWareClusterFinder(ClusterFinder):
    """
    Class to abstract all finding functions coming from the backend. Each provider has to implement this
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find_by_names(self, names):
        return (
            VMwareCluster(vm)
            for vm in clientutils.list_vms()
            if vm.name in names
        )

    def find_by_uuids(self, uuids):
        raise CODException("Listing clusters by UUIDs is not support by cm-cod-vmware")

    def find_all(self):
        return self.find_by_tags()

    def find_by_tags(self, tags=None, tags_any=None, not_tags=None, not_tags_any=None):
        tags = tags if tags is not None else []
        tags_any = tags_any if tags_any is not None else []
        not_tags = not_tags if not_tags is not None else []
        not_tags_any = not_tags_any if not_tags_any is not None else []

        return [
            VMwareCluster(vm) for vm in
            clientutils.list_vms(tags, tags_any, not_tags, not_tags_any)
        ]

    def get_cluster_name(self, cluster):
        return cluster.name

    def get_cluster_id(self, cluster):
        return None

    def get_cluster_tags(self, cluster):
        return cluster.get_tags()


findclusters_ns = ConfigNamespace("vmware.cluster.find", help_section="cluster filter parameters")
findclusters_ns.import_namespace(common_findclusters_ns)
