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

from enum import Enum

from pyVmomi import vim

from clusterondemand.exceptions import CODException
from clusterondemand.vlan import vlan_id_parser, vlan_id_serializer
from clusterondemandconfig import ConfigLoadError, ConfigNamespace


class NetworkBackend(Enum):
    """Supported network backends for deploying VMware clusters."""
    VSPHERE = "vsphere"
    NSX = "nsx"

    def __lt__(self, other):
        # We use sorted() to sort paramater choices. This means
        # that we need to implement the '<' operator.
        if not isinstance(other, NetworkBackend):
            raise ValueError(f"{other} is not of type NetworkBackend")
        return self.value < other.value

    def __str__(self):
        return self.value

    @staticmethod
    def get_backend_for_network(network):
        """
        Get the backend type for a network from the vSphere API.

        Currently we support two backends, NSX and vSphere.
        On vSphere we use distributed port groups for the networks, on NSX we use segments.
        The NSX segments are identified by vSphere as OpaqueNetworks that are based on a logical NSX switch.
        """
        if isinstance(network, vim.OpaqueNetwork) and network.summary.opaqueNetworkType == "nsx.LogicalSwitch":
            return NetworkBackend.NSX
        elif isinstance(network, vim.dvs.DistributedVirtualPortgroup):
            return NetworkBackend.VSPHERE
        else:
            raise CODException(f"Cannot define network backend for networks of type {type(network)}.")

    @staticmethod
    def internalnet_validator(parameter, configuration):
        backend = configuration[parameter.key]
        if backend == NetworkBackend.VSPHERE:
            required_parameter_names = ["vdswitch_name", "internalnet_vlan_ids"]
        elif backend == NetworkBackend.NSX:
            required_parameter_names = ["nsx_address", "nsx_username", "nsx_password",
                                        "transport_zone", "nsx_security_profile"]
        else:
            raise NotImplementedError(f"Cannot validate the parameters for backend {backend}")

        required_items = [configuration.get_item_for_key(name) for name in required_parameter_names]
        parameters_not_set = [item.parameter.name for item in required_items if not item.value]
        if parameters_not_set:
            missing_params = ", ".join(parameters_not_set)
            message = f"Using internalnet network backend '{backend}' requires '{missing_params}' to also be set."
            raise ConfigLoadError(message)

    @staticmethod
    def externalnet_validator(parameter, configuration):
        backend = configuration[parameter.key]
        if backend == NetworkBackend.VSPHERE:
            required_parameter = "externalnet_vdportgroup"
        elif backend == NetworkBackend.NSX:
            required_parameter = "externalnet_network"
        else:
            raise NotImplementedError(f"Cannot validate the parameters for backend {backend}")

        item = configuration.get_item_for_key(required_parameter)
        if not item.value:
            message = f"Using externalnet network backend '{backend}' requires '{required_parameter}' to also be set."
            raise ConfigLoadError(message)


network_ns = ConfigNamespace("vmware.network", help_section="network settings")
network_ns.add_parameter(
    "internalnet_network_backend",
    advanced=True,
    help="Backend used for deploying the clusters internal network",
    choices=[backend for backend in NetworkBackend],
    default=NetworkBackend.VSPHERE,
    validation=NetworkBackend.internalnet_validator,
    type=NetworkBackend
)
network_ns.add_enumeration_parameter(
    "internalnet_vlan_ids",
    advanced=True,
    parser=vlan_id_parser,
    serializer=vlan_id_serializer,
    help="VLAN ID or range of VLAN IDs that can be used by the portgroup of the internal network.",
)
network_ns.add_parameter(
    "vdswitch_name",
    advanced=True,
    help="Name of the Virtual Distributed Switch where the portgroup of the internal network will be created."
)
network_ns.add_parameter(
    "transport_zone",
    advanced=True,
    help="ID of the transport zone in which the NSX segment needs to be deployed.",
    help_varname="ID"
)
network_ns.add_parameter(
    "nsx_security_profile",
    advanced=True,
    help="ID of the profile used for configuring the security settings of the NSX segment.",
    help_varname="ID",
    default="cod-default-security-profile"
)
network_ns.add_parameter(
    "externalnet_network_backend",
    advanced=True,
    help="Backend used for managing the clusters external network.",
    choices=[backend for backend in NetworkBackend],
    default=NetworkBackend.VSPHERE,
    validation=NetworkBackend.externalnet_validator,
    type=NetworkBackend
)
network_ns.add_parameter(
    "externalnet_vdportgroup",
    advanced=True,
    help="Name of the pre-existing Virtual Distributed Portgroup which "
         "the external network interface will be attached to."
)
network_ns.add_parameter(
    "externalnet_network",
    advanced=True,
    help="Name of the pre-existing NSX-T segment the external network interface will be attached to."
)
