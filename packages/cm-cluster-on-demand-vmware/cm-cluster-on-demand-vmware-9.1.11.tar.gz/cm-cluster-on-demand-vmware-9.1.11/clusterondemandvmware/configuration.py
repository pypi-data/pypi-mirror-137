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
import clusterondemand.configuration
from clusterondemandconfig import ConfigNamespace, may_not_equal_none, must_be_multiple_of

vmwarecredentials_ns = ConfigNamespace("vmware.credentials", help_section="VMWare credentials")
vmwarecredentials_ns.add_parameter(
    "vmware_username",
    help="VMware vCenter user name",
    help_varname="USERNAME",
    validation=may_not_equal_none,
)
vmwarecredentials_ns.add_parameter(
    "vmware_password",
    help="The VMware vCenter password",
    help_varname="PASSWORD",
    validation=may_not_equal_none,
)
vmwarecredentials_ns.add_parameter(
    "vmware_address",
    help="IP Address of the VMware vCenter server",
    help_varname="IP",
    validation=may_not_equal_none
)
vmwarecredentials_ns.add_parameter(
    "vmware_verify_certificate",
    help="If set to False, don't verify the VMware vCenter HTTPS certificate",
    default=True,
)
vmwarecredentials_ns.add_parameter(
    "vmware_resource_pool",
    help="Name of the resource pool in VMware vCenter",
    validation=may_not_equal_none,
)
vmwarecredentials_ns.add_parameter(
    "nsx_address",
    help="IP Address or hostname of the VMware NSX-T manager",
    advanced=True,
)
vmwarecredentials_ns.add_parameter(
    "nsx_username",
    help="Username for the VMware NSX-T manager user",
    advanced=True,
)
vmwarecredentials_ns.add_parameter(
    "nsx_password",
    help="Password for the VMware NSX-T manager user",
    advanced=True,
)

vmwarecommon_ns = ConfigNamespace("vmware.common")
vmwarecommon_ns.import_namespace(clusterondemand.configuration.common_ns)
vmwarecommon_ns.remove_imported_parameter("version")
vmwarecommon_ns.import_namespace(vmwarecredentials_ns)

headnodecreate_ns = ConfigNamespace("vmware.headnode.create")
headnodecreate_ns.add_parameter(
    "head_node_number_cpus",
    default=2,
    help="Number of vCPUs allocated for the headnode virtual machine",
    help_varname="HEADNODE_NUMBER_CPUS",
    validation=may_not_equal_none,
    type=int
)
headnodecreate_ns.add_parameter(
    "head_node_memory_size",
    default=4096,
    help="Size of the memory allocated for the headnode virtual machine",
    help_varname="HEADNODE_MEMORY_SIZE_IN_MB",
    validation=[may_not_equal_none, must_be_multiple_of(128)],
    type=int
)

nodecreate_ns = ConfigNamespace("vmware.node.create")
nodecreate_ns.import_namespace(clusterondemand.configuration.nodes_ns)
nodecreate_ns.import_namespace(clusterondemand.configuration.node_disk_setup_ns)
nodecreate_ns.add_parameter(
    "node_number_cpus",
    default=2,
    help="Number of vCPUs allocated for the cloud nodes",
    help_varname="NODE_NUMBER_CPUS",
    validation=may_not_equal_none,
    type=int
)
nodecreate_ns.add_parameter(
    "node_memory_size",
    default=4096,
    help="Size of the memory allocated for the cloud nodes",
    help_varname="NODE_MEMORY_SIZE_IN_MB",
    validation=[may_not_equal_none, must_be_multiple_of(128)],
    type=int
)
nodecreate_ns.add_parameter(
    "node_root_volume_size",
    default=50,
    help="Node root disk size in GB",
    help_varname="SIZE_IN_GB",
    validation=may_not_equal_none,
    type=int
)

sshconfig_ns = ConfigNamespace("vmware.sshconfig")
sshconfig_ns.import_namespace(clusterondemand.configuration.sshconfig_ns)
