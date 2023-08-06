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

import base64
import logging
import yaml

from tenacity import retry, retry_if_exception_type, stop_after_delay, wait_fixed

import clusterondemand.clustercreate
import clusterondemand.configuration
import clusterondemand.copyfile
from clusterondemand.cloudconfig import CloudConfig
from clusterondemand.cloudconfig.headcommands import (
    add_head_node_commands,
    add_run_bright_setup_commands,
    add_wait_for_cmd_ready_commands
)
from clusterondemand.cloudconfig.headfiles import REMOTE_NODE_DISK_SETUP_PATH, add_common_head_files
from clusterondemand.clustercreate import generate_cluster_tags, make_cluster_name
from clusterondemand.exceptions import CODException
from clusterondemand.images.find import pickimages_ns as common_pickimages_ns
from clusterondemand.node_definition import NodeDefinition
from clusterondemand.paramvalidation import ParamValidator
from clusterondemand.ssh import clusterssh_ns
from clusterondemand.summary import SummaryType
from clusterondemand.vlan import expand_vlan_ids, vlan_id_serializer
from clusterondemand.wait_helpers import clusterwaiters_ns, wait_for_cluster_to_be_ready
from clusterondemandconfig import ConfigNamespace, config
from clusterondemandvmware.network import NetworkBackend, network_ns
from clusterondemandvmware.nsx import NsxClient
from clusterondemandvmware.ssh import add_to_ssh_config
from clusterondemandvmware.summary import VmwareSummaryGenerator

from . import clientutils
from .brightsetup import generate_bright_setup
from .cloudconfig.cloudconfig import VMwareSignalHandler
from .configuration import headnodecreate_ns, nodecreate_ns, sshconfig_ns, vmwarecommon_ns
from .findclusters import VMWareClusterFinder
from .images import VMWareImageSource

log = logging.getLogger("cluster-on-demand")


config_ns = ConfigNamespace("vmware.cluster.create", "cluster creation parameters")
config_ns.import_namespace(vmwarecommon_ns)
config_ns.import_namespace(clusterondemand.configuration.clustercreatepassword_ns)
config_ns.import_namespace(clusterondemand.configuration.clusterprefix_ns)
config_ns.import_namespace(clusterondemand.configuration.clustercreateconfirm_ns)
config_ns.import_namespace(clusterondemand.configuration.clustercreatedisks_ns)
config_ns.import_namespace(clusterondemand.configuration.clustercreatename_ns)
config_ns.import_namespace(clusterssh_ns)
config_ns.import_namespace(clusterwaiters_ns)
config_ns.import_namespace(clusterondemand.configuration.append_to_bashrc_ns)
config_ns.import_namespace(clusterondemand.configuration.aws_provider_tag_cm_setup_ns)
config_ns.import_namespace(clusterondemand.configuration.internal_net_ns)
config_ns.import_namespace(clusterondemand.configuration.resolve_hostnames_ns)
config_ns.import_namespace(clusterondemand.configuration.bright_setup_ns)
config_ns.import_namespace(clusterondemand.configuration.cmd_debug_ns)
config_ns.import_namespace(clusterondemand.copyfile.copyfile_ns)
config_ns.import_namespace(clusterondemand.configuration.clustercreatelicense_ns)
config_ns.import_namespace(clusterondemand.configuration.clustercreatewlm_ns)
config_ns.import_namespace(clusterondemand.configuration.timezone_ns)
config_ns.import_namespace(headnodecreate_ns)
config_ns.import_namespace(nodecreate_ns)
config_ns.import_namespace(sshconfig_ns)
config_ns.import_namespace(network_ns)
config_ns.override_imported_parameter("update_ssh_config", default=False)

config_ns.add_parameter(
    "cloudconfig",
    help_varname="OUTPUT_FILE",
    help=("Save the generated cloud-config data to the file. "
          "Use '-' as the file name to output the data to stdout. "
          "Useful with --dry-run.")
)
config_ns.add_switch_parameter(
    "dry_run",
    flags=["-d"],
    help="Dry run - do not actually create the cluster. Useful with --cloudconfig."
)
config_ns.add_enumeration_parameter(
    "node_kernel_modules",
    advanced=True,
    default=["vmxnet3", "vmw_pvscsi"],
    help_varname="MODULE",
    help="Kernel modules to configure for compute nodes"
)
config_ns.add_switch_parameter(
    "show_git_hashes",
    advanced=True,
    help="Show the git hashes of cmdaemon, cm-setup and cluster-tools in the create proposal.",
)
config_ns.add_parameter(
    "cmd_vmware_username",
    advanced=True,
    help=("User name for vCenter which will be used by CMDaemon on the created cluster."
          " If it's not set, the vmware_username parameter will be used instead."),
    help_varname="USERNAME",
    default=""
)
config_ns.add_parameter(
    "cmd_vmware_password",
    advanced=True,
    help=("Password for vCenter which will be used by CMDaemon on the created cluster."
          " If it's not set, the vmware_password parameter will be used instead."),
    help_varname="PASSWORD",
    default=""
)
config_ns.add_parameter(
    "internalnet_role",
    advanced=True,
    help=("When set, a permission will be configured on the port group representing the cluster internal network."
          " The permission will grant the specified role to username used to create the cluster, or, if set, to the"
          " user specified by the --cmd-vmware-username parameter. This can be used to ensure only the cluster"
          " CMDaemon can create VMs on the internal network."),
    default=""
)
config_ns.add_parameter(
    "max_nodes",
    advanced=True,
    default=50,
    help="Soft limit on the number of compute nodes which can be part of the cluster"
)

pickimages_ns = ConfigNamespace("vmware.images.pick", help_section="image selection parameters")
pickimages_ns.import_namespace(common_pickimages_ns)
pickimages_ns.override_imported_parameter("cloud_type", default="vmware")
config_ns.import_namespace(pickimages_ns)


def _validate_max_nodes():
    nodes = config["nodes"]
    max_nodes = config["max_nodes"]

    if nodes > max_nodes:
        raise CODException(f"The number of nodes {nodes} exceeds the maximum number of nodes {max_nodes}. "
                           "Consider increasing the maximum number of nodes by setting --max-nodes.")


def _set_tags(vm_obj, head_image):
    clientutils.get_service_manager().set_tags(vm_obj, generate_cluster_tags(head_image, only_image_tags=True))


def _check_disk_size(ovf_summary):
    try:
        size_params = next(
            param for param in ovf_summary.additional_params
            if param.get_struct_value().get_field("type").value.value == "SizeParams"
        )
    except StopIteration:
        raise Exception("Property params for OVF summary were not found")

    ovf_size = size_params.get_struct_value().get_field("approximate_flat_deployment_size").value.value
    ovf_size_gb = ovf_size / (1024 * 1024 * 1024)
    if config["head_node_root_volume_size"] < ovf_size_gb:
        raise CODException(
            f"Parameter {config.item_repr('head_node_root_volume_size')} is smaller than the OVF size "
            f"({ovf_size_gb:.1f} GB). Please change to a bigger size."
        )


def _get_external_network():
    if config["externalnet_network_backend"] == NetworkBackend.VSPHERE:
        external_network = config["externalnet_vdportgroup"]
    elif config["externalnet_network_backend"] == NetworkBackend.NSX:
        external_network = config["externalnet_network"]
    else:
        raise NotImplementedError(f"Cannot get external network for backend {config['externalnet_network_backend']}")

    return external_network


def _deploy_internal_net(network_name, internalnet_role):
    if config["internalnet_network_backend"] == NetworkBackend.VSPHERE:
        internalnet_id = _deploy_vsphere_internalnet(network_name, internalnet_role)
    elif config["internalnet_network_backend"] == NetworkBackend.NSX:
        internalnet_id = _deploy_nsx_internalnet(network_name)
    else:
        raise NotImplementedError(f"Cannot create internal network using {config['internalnet_network_backend']}")

    return internalnet_id


def _deploy_vsphere_internalnet(network_name, internalnet_role):
    """
    Deploy a network for the COD cluster on vSphere.

    The vSphere backed networks are based on distributed portgroups.
    The distributed portgroup will have a dedicated VLAN which
    will be selected from a range of allowed VLANs.
    """
    vdswitch_name = config["vdswitch_name"]
    vlan_id = _select_available_vlan(vdswitch_name, config["internalnet_vlan_ids"])
    log.info(f"Creating Portgroup {network_name} with VLAN ID {vlan_id} on switch {vdswitch_name}.")
    user = None
    if internalnet_role:
        user = config["cmd_vmware_username"] or config["vmware_username"]
    portgroup = clientutils.create_vdportgroup(vdswitch_name, network_name, vlan_id, user, internalnet_role)

    return portgroup.key


def _select_available_vlan(vdswitch_name, vlan_id_ranges):
    """Return the first available VLAN id that is within the vlan range."""
    used_vlan_ids = clientutils.get_used_vlan_ids(vdswitch_name)

    vlans_in_range = set(expand_vlan_ids(vlan_id_ranges))
    available_vlans = vlans_in_range.difference(used_vlan_ids)
    if available_vlans:
        return available_vlans.pop()
    else:
        vlan_range_definitions = ",".join([vlan_id_serializer(vlan_range) for vlan_range in vlan_id_ranges])
        raise CODException(f"All VLAN IDs in range '{vlan_range_definitions}' are already in use")


def _deploy_nsx_internalnet(network_name):
    """
    Deploy a network for the COD cluster using an NSX segment.
    """
    nsx_client = NsxClient()
    transport_zone_id = config["transport_zone"]
    security_profile_id = config["nsx_security_profile"]

    if not nsx_client.security_profile_exists(security_profile_id):
        log.info("Creating NSX security profile.")
        profile = nsx_client.create_internalnet_security_profile(security_profile_id)
        security_profile_id = profile.id

    log.info(f"Creating NSX segment {network_name}.")
    nsx_client.create_internalnet_segment(network_name, transport_zone_id, security_profile_id)
    network_id = _get_segment_network_id(network_name)

    return network_id


@retry(retry=retry_if_exception_type(CODException),
       stop=stop_after_delay(120),
       wait=wait_fixed(5),
       reraise=True)
def _get_segment_network_id(network_name):
    """
    Get the network id for the NSX segment.

    It takes a couple of seconds for the network to become available in vSphere.
    If the network has not shown up within 2 minutes we assume that there is a
    misconfiguration in the transport zone.
    """
    return clientutils.get_network_id(network_name)


def _get_head_node_properties(cloud_config, network_id):
    # Inject the internal network ID into the cloud config.
    # We use this ID to connect compute nodes to the internal network.
    for file in cloud_config["write_files"]:
        if file["path"] == "/root/cm/cm-bright-setup.conf":
            file["content"] = file["content"].replace("network_id: ''", f"network_id: {network_id}")

    formatted_cloud_config = "#cloud-config\n" + yaml.safe_dump(cloud_config.to_dict())
    encoded_cloud_config = base64.b64encode(formatted_cloud_config.encode()).decode("ascii")

    properties = {}
    properties["user-data"] = encoded_cloud_config
    if config["ssh_pub_key_path"]:
        properties["public-keys"] = open(config["ssh_pub_key_path"]).read()

    return properties


def run_command():
    _validate_max_nodes()

    log.info("Please wait...")
    head_image = VMWareImageSource.pick_head_node_image_using_options(config)
    node_image = VMWareImageSource.pick_compute_node_image_using_options(config)

    if node_image is None:
        raise CODException(
            f"Cannot find suitable node image for head node image {head_image.name}. Please specify with --node-image"
        )
    node_ovf = node_image.name

    clusters, _ = VMWareClusterFinder(all_stacks=False, ignore_newer=False).find_clusters()
    current_cluster_names = {cluster.name for cluster in clusters}
    cluster_name = make_cluster_name(head_image, lambda name: name in current_cluster_names)
    ParamValidator.validate_cluster_name(cluster_name)

    # Find the cluster's resource pool moid
    resource_pool_id = clientutils.get_resource_pool_id(config["vmware_resource_pool"])
    ovf_summary = clientutils.get_ovf_summary(resource_pool_id, head_image.name)
    log.debug(f"Found an OVF template: {ovf_summary}")
    _check_disk_size(ovf_summary)

    cm_bright_setup_conf = generate_bright_setup(cluster_name, REMOTE_NODE_DISK_SETUP_PATH, node_ovf)
    cloud_config = build_cloud_config(cm_bright_setup_conf, head_image.version)
    formatted_cloud_config = "#cloud-config\n" + yaml.safe_dump(cloud_config.to_dict())
    if config["cloudconfig"] == "-":
        print(formatted_cloud_config)
    elif config["cloudconfig"] is not None:
        with open(config["cloudconfig"], "w") as output:
            output.write(formatted_cloud_config)

    internalnet_role = None
    if config["internalnet_role"]:
        internalnet_role = clientutils.get_role(config["internalnet_role"])
        if not internalnet_role:
            raise CODException("Can't find specified role: " + config["internalnet_role"])

    if config["dry_run"]:
        log.info("Running in dry-run mode. Cluster will not be created.")
        return

    head_node_definition, node_definition = _get_node_definitions(config)
    summary = VmwareSummaryGenerator(cluster_name, SummaryType.Proposal, config=config,
                                     head_node_definition=head_node_definition, head_image=head_image,
                                     node_definition=node_definition, node_image=node_image)
    summary.print_summary(log.info)
    if config["ask_to_confirm_cluster_creation"]:
        clusterondemand.utils.confirm_cluster_creation()
    log.info(f"Creating cluster {cluster_name}")

    head_node = None
    ip = None

    try:
        external_network = _get_external_network()
        internalnet_id = _deploy_internal_net(cluster_name, internalnet_role)
        network_mappings = {
            "externalnet": clientutils.get_network_id(external_network),
            "internalnet": internalnet_id,
        }

        log.info("Deploying OVF")
        properties = _get_head_node_properties(cloud_config, internalnet_id)
        head_node = clientutils.deploy_ovf(
            resource_pool_id,
            ovf_summary,
            head_image.name,
            cluster_name,
            network_mappings,
            properties
        )
        _set_tags(head_node, head_image)

        clientutils.configure_vm(
            head_node,
            config["head_node_number_cpus"],
            config["head_node_memory_size"],
            config["head_node_root_volume_size"]
        )
    except Exception as e:
        log.error("Error creating cluster. Rolling back operations")
        if head_node is not None:
            clientutils.delete_vms([head_node])

        network = clientutils.get_network(cluster_name)
        if network:
            try:
                clientutils.delete_network(network)
            except clientutils.ServiceManagerObjectNotFoundError:
                pass
            except Exception as e:
                log.error(f"Error deleting network {network.name}: {e}")

        raise e

    log.info("Powering on head node")
    clientutils.power_on_vm(head_node)

    log.info("Node was powered on. Waiting for network")
    ip = clientutils.get_headnode_external_ip(head_node, wait=True)

    wait_for_cluster_to_be_ready(config, ip, head_image.version)
    clientutils.unmount_ovf_environment_image(head_node, ip)

    if config["update_ssh_config"]:
        connection_string = add_to_ssh_config(config, cluster_name, ip)
    else:
        connection_string = f"ssh root@{ip}"

    log.info("Cluster has been created successfully.")
    generator = VmwareSummaryGenerator(cluster_name, SummaryType.Overview, config=config,
                                       ssh_string=connection_string, ip=ip)
    generator.print_summary(log.info)


def _get_node_definitions(config):
    head_node_flavor = f"""{config["head_node_number_cpus"]} vCPUs, {config["head_node_memory_size"]} MB RAM"""
    head_node_definition = NodeDefinition(1, head_node_flavor)
    head_node_definition.disks.append({"size": config["head_node_root_volume_size"], "type": None})

    node_flavor = f"""{config["node_number_cpus"]} vCPUs, {config["node_memory_size"]} MB RAM"""
    node_definition = NodeDefinition(config["nodes"], node_flavor)
    node_definition.disks.append({"size": config["node_root_volume_size"], "type": None})

    return head_node_definition, node_definition


def build_cloud_config(cm_bright_setup_conf, version):
    cloud_config = CloudConfig(VMwareSignalHandler("Head node"))
    add_common_head_files(cloud_config, version)
    cloud_config.add_file("/root/cm/cm-bright-setup.conf", yaml.dump(cm_bright_setup_conf))
    add_head_node_commands(cloud_config, str(config["head_node_internal_ip"]))
    if config["run_cm_bright_setup"]:
        add_run_bright_setup_commands(cloud_config)
        add_wait_for_cmd_ready_commands(cloud_config)
    cloud_config.add_config_complete_commands()
    return cloud_config
