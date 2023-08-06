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

import atexit
import functools
import hashlib
import itertools
import logging
import re
import socket
import ssl
import time
import uuid
from http.client import HTTPSConnection

import netaddr
import pyVim.task
import requests
from com.vmware.cis.tagging_client import CategoryModel
from com.vmware.content import library_client
from com.vmware.content.library_client import Item
from com.vmware.vapi.std_client import DynamicID
from com.vmware.vcenter.ovf_client import LibraryItem
from pyVim.connect import Disconnect, SmartConnect
from pyVmomi import vim, vmodl
from vmware.vapi.vsphere.client import create_vsphere_client

from clusterondemand.exceptions import CODException
from clusterondemand.ssh import SSHExecutor
from clusterondemand.utils import is_uuid
from clusterondemandconfig import config
from clusterondemandvmware.network import NetworkBackend
from clusterondemandvmware.nsx import NsxClient

log = logging.getLogger("cluster-on-demand")

COD_TAG_CATEGORY = "CLUSTER_ON_DEMAND_TAGS"


class ServiceManagerError(Exception):
    pass


class ServiceManagerObjectCollisionError(ServiceManagerError):
    pass


class ServiceManagerObjectNotFoundError(ServiceManagerError):
    pass


class CannotFindTag(Exception):
    def __init__(self, name):
        super().__init__(f"Cannot find tag {name} in vSphere")


class ServiceManager(object):
    def __init__(self, server, username, password, verify_cert):
        self.server_url = server
        self.username = username
        self.password = password
        self.si = None
        self.content = None
        self.vim_uuid = None
        self.verify_cert = verify_cert
        self._views = []

    def get_vim_objs(self, vimtype):
        """
        Get all vsphere managed objects for some vimtype
        """

        container = self.content.viewManager.CreateContainerView(
            self.content.rootFolder, vimtype, True)
        self._views.append(container)

        for obj in container.view:
            yield obj

    def get_vim_obj_by_name(self, vimtype, name):
        """
        DEPRECATED. Only get_vdswitch uses this

        Get the vsphere managed object associated with a given text name
        """
        assert name
        result = None
        for obj in self.get_vim_objs(vimtype):
            if obj.name == name:
                if result is not None:
                    different_types_msg = (f": {type(result).__name__}, {type(obj).__name__}"
                                           if type(result) != type(obj) else "")
                    raise ServiceManagerObjectCollisionError(
                        f"Multiple objects of type {vimtype} and name {name} was found"
                        f", only one was expected{different_types_msg}"
                    )
                result = obj
        if result is None:
            raise ServiceManagerObjectNotFoundError(f"Object of type {vimtype} and name {name} was not found")
        return result

    def get_vim_objs_by_moId(self, vimtype, moids):
        """
        Get the vsphere managed objects by moid value
        """
        return [obj for obj in self.get_vim_objs(vimtype) if obj._GetMoId() in moids]

    def get_vim_obj_by_moId(self, vimtype, moid):
        objs = self.get_vim_objs_by_moId(vimtype, [moid])
        return objs[0] if objs else None

    @functools.lru_cache()
    def get_tag_category_id(self, name):
        for category_id in self.vsphere.tagging.Category.list():
            category = self.vsphere.tagging.Category.get(category_id)
            if category.name == name:
                return category_id
        return None

    def create_tag_category(self, name):
        existing = self.get_tag_category_id(name)
        if existing:
            return existing

        create_spec = self.vsphere.tagging.Category.CreateSpec()
        create_spec.name = name
        create_spec.description = "Created by cm-cod-vmware"
        create_spec.cardinality = CategoryModel.Cardinality.MULTIPLE
        create_spec.associable_types = set()
        return self.vsphere.tagging.Category.create(create_spec)

    # We need this as None, because we might have more than 128 tags
    # If we set a small cache, we will end up just overwritting it everytime
    @functools.lru_cache(maxsize=None)
    def get_tag(self, tag_id):
        return self.vsphere.tagging.Tag.get(tag_id)

    def get_tag_id(self, name):
        # vSphere doesn't have any way of getting a single tag by name
        # So we have to list all and compare the names
        # https://vmware.github.io/vsphere-automation-sdk-rest/6.5/index.html#SVC_com.vmware.cis.tagging.tag
        for tag_id in self.vsphere.tagging.Tag.list():
            tag = self.get_tag(tag_id)
            if tag.name == name:
                return tag_id
        return None

    def get_tag_ids_map(self, names, raise_if_not_found=True):
        tag_ids = {}
        for name in names:
            tag_id = self.get_tag_id(name)
            if tag_id is None:
                if raise_if_not_found:
                    raise CannotFindTag(name)
                continue
            tag_ids[tag_id] = name
        return tag_ids

    def get_tag_name(self, tag_id):
        return self.get_tag(tag_id).name

    def create_tag(self, name, category_id):
        existing = self.get_tag_id(name)
        if existing:
            return existing

        create_spec = self.vsphere.tagging.Tag.CreateSpec()
        create_spec.name = name
        create_spec.description = "Created by cm-cod-vmware"
        create_spec.category_id = category_id
        return self.vsphere.tagging.Tag.create(create_spec)

    def create_tags(self, tag_names, tag_category=COD_TAG_CATEGORY):
        category_id = self.create_tag_category(tag_category)
        return [self.create_tag(name, category_id) for name in tag_names]

    def set_tags(self, obj, tag_names, tag_category=COD_TAG_CATEGORY):
        if isinstance(obj, vim.ManagedObject):
            obj_type = type(obj).__name__.split(".")[-1]
            obj_id = obj._GetMoId()
        elif isinstance(obj, str) and is_uuid(obj):
            # If it's a UUID, we assume it's a content library item
            obj_type = "com.vmware.content.library.Item"
            obj_id = obj
        else:
            raise Exception(f"Not possible to set tags for type {type(obj)}")

        category_id = self.get_tag_category_id(tag_category)
        if not category_id:
            raise CODException(f"Cannot find Tag Category '{tag_category}' on vSphere")

        tag_ids = []
        for name in tag_names:
            tag_id = self.get_tag_id(name)
            if not tag_id:
                raise CODException(f"Cannot find Tag '{name}' on vSphere")
            tag_ids.append(tag_id)

        result = self.vsphere.tagging.TagAssociation.attach_multiple_tags_to_object(
            tag_ids=tag_ids,
            object_id=DynamicID(type=obj_type, id=obj_id)
        )

        if not result.success:
            errors = [error.default_message for error in result.error_messages]
            raise CODException(f"Error setting tags on {obj_id}: {', '.join(errors)}")

    def unset_tags(self, obj, tag_names):
        if isinstance(obj, vim.ManagedObject):
            obj_type = type(obj).__name__.split(".")[-1]
            obj_id = obj._GetMoId()
        elif isinstance(obj, str) and is_uuid(obj):
            # If it's a UUID, we assume it's a content library item
            obj_type = "com.vmware.content.library.Item"
            obj_id = obj
        else:
            raise Exception(f"Not possible to unset tags for type {type(obj)}")

        tag_ids = [self.get_tag_id(name) for name in tag_names]

        result = self.vsphere.tagging.TagAssociation.detach_multiple_tags_from_object(
            tag_ids=tag_ids,
            object_id=DynamicID(type=obj_type, id=obj_id)
        )

        if not result.success:
            errors = [error.default_message for error in result.error_messages]
            raise CODException(f"Error unsetting tags from {obj_id}: {', '.join(errors)}")

    def get_tags(self, obj):
        if isinstance(obj, vim.ManagedObject):
            obj_type = type(obj).__name__.split(".")[-1]
            obj_id = obj._GetMoId()
        elif isinstance(obj, str) and is_uuid(obj):
            # If it's a UUID, we assume it's a content library item
            obj_type = "com.vmware.content.library.Item"
            obj_id = obj
        elif isinstance(obj, str) and is_vm_id(obj):
            obj_type = "VirtualMachine"
            obj_id = obj
        else:
            raise Exception(f"Not possible to get tags for type {type(obj)}")

        return [
            self.get_tag_name(tag_id)
            for tag_id in self.vsphere.tagging.TagAssociation.list_attached_tags(
                object_id=DynamicID(type=obj_type, id=obj_id)
            )
        ]

    def get_objs_attached_to_tags(self,
                                  object_type,
                                  tags=None,
                                  tags_any=None,
                                  not_tags=None,
                                  not_tags_any=None):
        """
        Returns a list of IDs that are attached to all tags in 'tags'.
        It's responsibility of the caller to fetch the real objects from those ids

        The tags arguments work in the same way as the tags for OpenStack
        They should all be list of strings
        tags: All the specified tags have to match (AND)
        tags_any: At least one of the specified tags have to match (OR)
        not_tags: All the tags in this dict MUST NOT be present in the objects (NAND)
        not_tags_any: At least one the tags MUST NOT be present in the object (NOR)


        'object_type' can be any string, as per vSphere tagging API. However, vCenter has some specific names
        that it uses to show in the Web UI:

        For Content Library items: "com.vmware.content.library.Item"
        For VMs: "VirtualMachine"
        """
        tags = tags if tags is not None else []
        tags_any = tags_any if tags_any is not None else []
        not_tags = not_tags if not_tags is not None else []
        not_tags_any = not_tags_any if not_tags_any is not None else []

        if not_tags and (not tags and not tags_any):
            # not_tags doesn't make sense alone because, because we cannot fetch "all objects"
            raise ValueError(f"not_tags={not_tags} cannot be used without specifying 'tags' or 'tags_any'")

        if not_tags_any and (not tags and not tags_any):
            # not_tags_any doesn't make sense alone because, because we cannot fetch "all objects"
            raise ValueError(f"not_tags_any={not_tags_any} cannot be used without specifying 'tags' or 'tags_any'")

        tag_id_to_name = {}

        try:
            tag_id_to_name.update(self.get_tag_ids_map(tags))
        except CannotFindTag as e:
            log.debug("Required tag doesn't exist. No object will match to it: {e}", e)
            return []

        # For the following we just ignore if the tag doesn't exist. It will be handled in the local filtering below
        tag_id_to_name.update(self.get_tag_ids_map(tags_any, raise_if_not_found=False))
        tag_id_to_name.update(self.get_tag_ids_map(not_tags, raise_if_not_found=False))
        tag_id_to_name.update(self.get_tag_ids_map(not_tags_any, raise_if_not_found=False))

        tag_ids_to_obj_id = {
            result.tag_id: {
                obj_id.id
                for obj_id in result.object_ids
                if obj_id.type == object_type
            }
            for result in self.vsphere.tagging.TagAssociation.list_attached_objects_on_tags(tag_id_to_name.keys())
        }

        def get_tags_in_obj(obj_id):
            return [
                tag_id_to_name[tag_id]
                for tag_id, objs in tag_ids_to_obj_id.items()
                if obj_id in objs
            ]

        all_object_ids = set(itertools.chain(*tag_ids_to_obj_id.values()))

        ret = []
        for obj_id in all_object_ids:
            tags_in_obj = get_tags_in_obj(obj_id)
            if not all(tag in tags_in_obj for tag in tags):
                continue
            if tags_any and not any(tag in tags_in_obj for tag in tags_any):
                continue
            if any(tag in tags_in_obj for tag in not_tags):
                continue
            if not_tags_any and all(tag in tags_in_obj for tag in not_tags_any):
                continue
            ret.append(obj_id)
        return ret

    def create_unverified_session(self, session, suppress_warning=True):
        """
        Create a unverified session to disable the server certificate verification.
        This is not recommended in production code.
        """
        session.verify = False
        if suppress_warning:
            # Suppress unverified https request warnings
            from requests.packages.urllib3.exceptions import InsecureRequestWarning
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        return session

    def create_session(self):
        session = requests.Session()
        if not self.verify_cert:
            session = self.create_unverified_session(session)
        return session

    def connect(self):
        self.vsphere = create_vsphere_client(
            server=self.server_url,
            username=self.username,
            password=self.password,
            session=self.create_session()
        )

        # Connect to VIM API Endpoint on vCenter Server system
        context = None

        if not self.verify_cert:
            context = ssl._create_unverified_context()
        self.si = SmartConnect(host=self.server_url,
                               user=self.username,
                               pwd=self.password,
                               sslContext=context)
        assert self.si is not None

        # Retrieve the service content
        self.content = self.si.RetrieveContent()
        assert self.content is not None
        self.vim_uuid = self.content.about.instanceUuid

    def disconnect(self):
        for view in self._views:
            try:
                view.Destroy()
            except vmodl.fault.ManagedObjectNotFound:
                pass  # silently bypass the exception if the objects are already deleted/not found on the server
        if self.vsphere:
            # It has a disconnect on __exit__, so this is just a way to trigger it
            with self.vsphere:
                pass
        if self.si:
            Disconnect(self.si)

    def wait_for_tasks(self, tasks):
        """
        Given the tasks, it returns after all the tasks are complete
        """
        taskList = [str(task) for task in tasks]

        # Create filter
        objSpecs = [
            vmodl.query.PropertyCollector.ObjectSpec(obj=task) for task in tasks
        ]
        propSpec = vmodl.query.PropertyCollector.PropertySpec(
            type=vim.Task, pathSet=[], all=True)
        filterSpec = vmodl.query.PropertyCollector.FilterSpec()
        filterSpec.objectSet = objSpecs
        filterSpec.propSet = [propSpec]
        task_filter = self.content.propertyCollector.CreateFilter(filterSpec, True)

        try:
            version, state = None, None

            # Loop looking for updates till the state moves to a completed state.
            while len(taskList):
                update = self.content.propertyCollector.WaitForUpdates(version)
                for filterSet in update.filterSet:
                    for objSet in filterSet.objectSet:
                        task = objSet.obj
                        for change in objSet.changeSet:
                            if change.name == "info":
                                state = change.val.state
                            elif change.name == "info.state":
                                state = change.val
                            else:
                                continue

                            if not str(task) in taskList:
                                continue

                            if state == vim.TaskInfo.State.success:
                                # Remove task from taskList
                                taskList.remove(str(task))
                            elif state == vim.TaskInfo.State.error:
                                raise task.info.error
                # Move to next version
                version = update.version
        finally:
            if task_filter:
                task_filter.Destroy()


_servicemanager = None


def get_service_manager():
    # The way this cache works is similar to what we do to openstack clientutils
    global _servicemanager

    if not _servicemanager:
        _servicemanager = ServiceManager(
            config["vmware_address"],
            config["vmware_username"],
            config["vmware_password"],
            config["vmware_verify_certificate"],
        )
        _servicemanager.connect()
        # They do this in the samples
        atexit.register(_servicemanager.disconnect)

    return _servicemanager


def _filter_by_tags(objs, tags=None, tags_any=None, not_tags=None, not_tags_any=None):
    if any([tags, tags_any, not_tags, not_tags_any]):
        for obj in objs:
            # TODO(CM-32510) Do this filtering on the server side...
            # Not sure which of them are possible, but we should do as much as we can
            tags_in_obj = get_service_manager().get_tags(obj)
            if not all(tag in tags_in_obj for tag in tags):
                continue
            if tags_any and not any(tag in tags_in_obj for tag in tags_any):
                continue
            if any(tag in tags_in_obj for tag in not_tags):
                continue
            if not_tags_any and all(tag in tags_in_obj for tag in not_tags_any):
                continue
            yield obj
    else:
        for obj in objs:
            yield obj


def is_vm_id(vm_id):
    return re.match(r"vm-\d+", vm_id)


def get_library_item_id_by_name(name):
    library_item_service = Item(get_service_manager().vsphere._stub_config)
    item_ids = library_item_service.find(Item.FindSpec(name=name))
    return item_ids[0] if item_ids else None


def get_resource_pool_id(name):
    resource_pool_summaries = get_service_manager().vsphere.vcenter.ResourcePool.list(
        filter=get_service_manager().vsphere.vcenter.ResourcePool.FilterSpec(
            names=set([name])
        )
    )

    if len(resource_pool_summaries) == 0:
        raise CODException(f"Resource pool with name {name} was not found")
    elif len(resource_pool_summaries) > 1:
        raise CODException(f"Multiple resource pools were found with name {name}"
                           f", only one must exist")

    return resource_pool_summaries[0].resource_pool


def get_ovf_summary(resource_pool_id, ovf_name):
    # TODO Why do we need the resource pool to get this summary??
    deployment_target = LibraryItem.DeploymentTarget(resource_pool_id=resource_pool_id)
    lib_item_id = get_library_item_id_by_name(ovf_name)
    assert lib_item_id
    log.debug(f"Library item ID: {lib_item_id}")
    ovf_lib_item_service = LibraryItem(get_service_manager().vsphere._stub_config)
    ovf_summary = ovf_lib_item_service.filter(ovf_library_item_id=lib_item_id, target=deployment_target)
    return ovf_summary


def get_vdswitch(name):
    # TODO If possible, we should be calling some list() functions from vcenter like the other functions
    # But I couldn't find how to do this
    vdswitch_obj = get_service_manager().get_vim_obj_by_name([vim.DistributedVirtualSwitch], name)
    return vdswitch_obj


def get_network_id(name):
    network = get_network(name)
    if network is None:
        raise CODException(f"Cannot find network with name {name}")
    backend = NetworkBackend.get_backend_for_network(network)
    if backend == NetworkBackend.NSX:
        # NSX networks don't have a key or id, we need to extract it from the
        # string representation of the object. An example id is: network-o2303.
        return re.search(r"network-\w*", str(network)).group()
    elif backend == NetworkBackend.VSPHERE:
        return network.key
    else:
        raise NotImplementedError(f"Get network id is not implement for network type {type(network)}")


def get_network(name):
    sm = get_service_manager()
    objs = sm.vsphere.vcenter.Network.list(
        sm.vsphere.vcenter.Network.FilterSpec(
            names=set([name])
        )
    )

    if objs:
        return get_service_manager().get_vim_obj_by_moId([vim.Network], objs[0].network)
    else:
        return None


def get_role(name):
    return next(
        (role for role in get_service_manager().content.authorizationManager.roleList if role.name == name),
        None
    )


def list_vms(tags=None, tags_any=None, not_tags=None, not_tags_any=None):
    vsphere = get_service_manager().vsphere
    resource_pool_id = get_resource_pool_id(config["vmware_resource_pool"])
    vms = vsphere.vcenter.VM.list(
        vsphere.vcenter.VM.FilterSpec(
            resource_pools={resource_pool_id}
        )
    )
    # VM.list returns a Summary object
    vm_ids = list(_filter_by_tags([vm.vm for vm in vms], tags, tags_any, not_tags, not_tags_any))
    return get_service_manager().get_vim_objs_by_moId([vim.VirtualMachine], vm_ids)


# TODO Maybe there is some Python function for this? It doesn't seem correct to use tenacity
def poll(func, n_attempts=60, sleep_time=10):
    """Wait for func to return True, or raise exception"""
    attempt = 1
    while True:
        if func():
            return
        if attempt >= n_attempts:
            raise TimeoutError()
        attempt += 1
        time.sleep(sleep_time)


def get_headnode_external_ip(vm_obj, wait=False):
    # Wait until both nics (internalnet and externalnet) are available.
    # The external network is always assigned to the second nic.
    # Once, the nic has connected to the network we return the ipv4 address.
    try:
        poll(lambda: len(vm_obj.guest.net) >= 2, n_attempts=60 if wait else 0)
        external_nic = vm_obj.guest.net[1]
        poll(lambda: any(netaddr.valid_ipv4(ip.ipAddress) for ip in external_nic.ipConfig.ipAddress),
             n_attempts=60 if wait else 0)
    except TimeoutError:
        raise CODException(f"Timeout while waiting for a valid IPv4 address for {vm_obj.name}")

    return next(ip.ipAddress for ip in external_nic.ipConfig.ipAddress if netaddr.valid_ipv4(ip.ipAddress))


def get_vdportgroup(vdswitch_name, vdportgroup_name):
    vdswitch = get_vdswitch(vdswitch_name)
    return next((
        vdportgroup
        for vdportgroup in vdswitch.portgroup
        if vdportgroup.name == vdportgroup_name
    ), None)


def create_vdportgroup(vdswitch_name, vdportgroup_name, vlan_id, user, role):
    """Create Distributed Switch portgroup"""
    port_group_type = "earlyBinding"
    vlan_spec = vim.dvs.VmwareDistributedVirtualSwitch.VlanIdSpec(vlanId=vlan_id)
    port_config_policy = vim.dvs.VmwareDistributedVirtualSwitch.VmwarePortConfigPolicy(vlan=vlan_spec)
    port_group_spec = vim.dvs.DistributedVirtualPortgroup.ConfigSpec(
        name=vdportgroup_name,
        type=port_group_type,
        defaultPortConfig=port_config_policy
    )

    vdswitch = get_vdswitch(vdswitch_name)
    task = vdswitch.CreateDVPortgroup_Task(port_group_spec)
    pyVim.task.WaitForTask(task)
    port_group = task.info.result

    if role:
        perm = vim.AuthorizationManager.Permission()
        perm.entity = port_group
        perm.group = False
        perm.principal = user
        perm.propagate = False
        perm.roleId = role.roleId

        get_service_manager().content.authorizationManager.SetEntityPermissions(port_group, [perm])

    return port_group


def get_used_vlan_ids(vdswitch_name):
    """Return a set contianing the used VLAN (PVLAN excluded) ids in the switch"""
    vdswitch = get_vdswitch(vdswitch_name)
    vlan_ids = vdswitch.QueryUsedVlanIdInDvs()
    return set(vlan_ids)


def delete_vdportgroup(vdswitch_name, vdportgroup_name):
    vdportgroup = get_vdportgroup(vdswitch_name, vdportgroup_name)
    if not vdportgroup:
        raise Exception(
            f"Distributed Portgroup with name {vdportgroup_name} was not found"
        )

    task = vdportgroup.Destroy()
    pyVim.task.WaitForTask(task)


def deploy_ovf(resource_pool_id, ovf_summary, ovf_name, vm_name, network_mappings, properties):
    deployment_target = LibraryItem.DeploymentTarget(resource_pool_id=resource_pool_id)
    lib_item_id = get_library_item_id_by_name(ovf_name)

    try:
        property_params = next(
            param for param in ovf_summary.additional_params
            if param.get_struct_value().get_field("type").value.value == "PropertyParams"
        )
    except StopIteration:
        raise Exception("Property params for OVF summary were not found")

    ovf_properties = property_params.get_struct_value().get_field("properties").value

    available_properties = [prop.get_field("id").value.value for prop in ovf_properties]
    log.debug(f"Available properties for this OVF: {available_properties}")
    if any(prop for prop in properties if prop not in available_properties):
        raise Exception("Some properties are not defined in the available properties")

    for key, value in properties.items():
        ovf_prop = next(prop for prop in ovf_properties if prop.get_field("id").value.value == key)
        ovf_prop.get_field("value").value.value = value

    # Build the deployment spec
    deployment_spec = LibraryItem.ResourcePoolDeploymentSpec(
        name=vm_name,
        # TODO Do we need this annotation??
        annotation=ovf_summary.annotation,
        accept_all_eula=True,
        network_mappings=network_mappings,
        storage_mappings=None,
        storage_provisioning=None,
        storage_profile_id=None,
        locale=None,
        flags=None,
        additional_parameters=ovf_summary.additional_params,
        default_datastore_id=None)

    # Deploy the ovf template
    ovf_lib_item_service = LibraryItem(get_service_manager().vsphere._stub_config)
    result = ovf_lib_item_service.deploy(lib_item_id,
                                         deployment_target,
                                         deployment_spec,
                                         client_token=str(uuid.uuid4()))

    # The type and ID of the target deployment is available in the deployment result.
    if result.succeeded:
        log.debug(f"Deployment successful. Result resource: {result.resource_id.type}, ID: {result.resource_id.id}")
        vm_id = result.resource_id.id
        error = result.error
        if error is not None:
            for warning in error.warnings:
                log.warning(f"OVF warning: {warning.message}")

        vm_obj = get_service_manager().get_vim_obj_by_moId([vim.VirtualMachine], vm_id)
        return vm_obj
    else:
        for error in result.error.errors:
            log.error(f"OVF error: {error.message}")
        raise CODException("OVF Deployment failed")


def configure_vm(vm_obj, num_cpus, memory_in_mb, disk_size_in_gb):
    change_disk_size_operation = get_change_disk_size_operation(vm_obj, disk_size_in_gb)

    vm_specification = vim.VirtualMachineConfigSpec(
        numCPUs=num_cpus,
        memoryMB=memory_in_mb,
        deviceChange=[change_disk_size_operation]
    )

    log.debug(f"Configuring {vm_obj.name} with {num_cpus} cpus, {memory_in_mb}MB RAM and a {disk_size_in_gb}GB disk.")
    get_service_manager().wait_for_tasks([vm_obj.ReconfigVM_Task(vm_specification)])


def get_change_disk_size_operation(vm_obj, size_in_gb):
    disks = [device for device in vm_obj.config.hardware.device if isinstance(device, vim.VirtualDisk)]
    if not disks:
        raise Exception(f"Cannot find disks for vm {vm_obj.name}")

    if len(disks) != 1:
        log.warning(f"More than one disk found on {vm_obj.name}")

    disk = disks[0]
    new_size = size_in_gb * 1024 * 1024 * 1024

    if new_size < disk.capacityInBytes:
        raise Exception(f"Refusing to resize disk for {vm_obj.name}: {new_size} < {disk.capacityInBytes}")

    disk.capacityInBytes = new_size
    change_disk_size_operation = vim.VirtualDeviceConfigSpec(device=disk, operation="edit")

    return change_disk_size_operation


def unmount_ovf_environment_image(vm_obj, vm_ip):
    """Unmount the VMware OVF environment injection media"""
    # We need to eject the ISO on the host first, if not the operation
    # is stalled until an operator overrides the guest os lock.
    try:
        SSHExecutor(vm_ip, raise_exceptions=False).check_call("eject")
        unmount_cd_drive(vm_obj)
    except Exception:
        log.warning("Failed to unmount the VMware OVF environment ISO. "
                    "Please disconnect the CD/DVD drive using the vSphere client")


def unmount_cd_drive(vm_obj):
    cd_drive = next(device for device in vm_obj.config.hardware.device if isinstance(device, vim.VirtualCdrom))
    if not cd_drive:
        raise Exception(f"Cannot find CD/DVD drive for vm {vm_obj.name}")

    # Replace the backing with an empty passthrough device (default VMware CD/DVD drive).
    cd_drive.backing = vim.VirtualCdromRemotePassthroughBackingInfo()
    cd_drive.deviceInfo.summary = ""
    unmount_host_image_operation = vim.VirtualDeviceConfigSpec(device=cd_drive, operation="edit")

    vm_specification = vim.VirtualMachineConfigSpec(
        deviceChange=[unmount_host_image_operation]
    )

    log.debug(f"Unmounting CD/DVD media from {vm_obj.name}.")
    get_service_manager().wait_for_tasks([vm_obj.ReconfigVM_Task(vm_specification)])


def get_library_id_by_name(name):
    sm = get_service_manager()
    find_spec = sm.vsphere.content.Library.FindSpec(name=name)
    ids = sm.vsphere.content.Library.find(find_spec)
    return ids[0] if ids else None


@functools.lru_cache()
def get_available_content_library_types():
    # Return list of strings with the available types
    return [t.type for t in get_service_manager().vsphere.content.Type.list()]


def create_library_item(library_name, item_name, item_type):
    if item_type not in get_available_content_library_types():
        raise CODException(f"Type {item_type} is not in the list of available types")

    library_id = get_library_id_by_name(library_name)
    if not library_id:
        raise CODException(f"Cannot find content library '{library_name}'")

    item_model = library_client.ItemModel()
    item_model.name = item_name
    item_model.description = "Created by cm-cod-vmware"
    item_model.type = item_type
    item_model.library_id = library_id
    return get_service_manager().vsphere.content.library.Item.create(create_spec=item_model)


def delete_clusters(clusters):
    """
    Delete all VMware clusters.

    Each cluster is actually a network with associated VMs.
    Deleting a cluster means powering off and deleting all VMs and ultimately removing the network.
    """
    vms = [vm for c in clusters for vm in c.get_vms()]
    if vms:
        active_vms = [vm for vm in vms if vm.runtime.powerState == "poweredOn"]
        if active_vms:
            log.info("Attempting to power off VMs: %s", ", ".join(vm.name for vm in active_vms))
            power_off_vms(active_vms)

        log.info("Deleting VMS: %s", ", ".join(vm.name for vm in vms))
        delete_vms(vms)

    log.info("Deleting networks: %s", ", ".join(c.internal_net.name for c in clusters))
    for cluster in clusters:
        try:
            delete_network(cluster.internal_net)
        except Exception as e:
            log.error(f"Failure while deleting the network for cluster {cluster.name}: {e}")


def power_off_vms(vms):
    get_service_manager().wait_for_tasks([vm.PowerOff() for vm in vms])


def delete_vms(vms):
    get_service_manager().wait_for_tasks([vm.Destroy_Task() for vm in vms])


def delete_network(network):
    backend = NetworkBackend.get_backend_for_network(network)
    if backend == NetworkBackend.NSX:
        client = NsxClient()
        client.delete_segment(network.name)
    elif backend == NetworkBackend.VSPHERE:
        get_service_manager().wait_for_tasks([network.Destroy_Task()])
    else:
        raise NotImplementedError(f"Cannot delete network with backend {backend}")


def power_on_vm(vm_obj):
    return power_on_vms([vm_obj])


def power_on_vms(vms):
    get_service_manager().wait_for_tasks([vm.PowerOn() for vm in vms])


def get_server_cert_thumbprint(host, port=443, verify=True):
    # Make sure that the host has a valid certificate
    if verify:
        conn = HTTPSConnection(host, port, timeout=1)
        try:
            conn.connect()
        except Exception as e:
            raise CODException(f"Failed to verify {host} host certificate: {e}")
        finally:
            conn.close()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wrapped_sock = None
    try:
        sock.settimeout(1)
        wrapped_sock = ssl.wrap_socket(sock)
        wrapped_sock.connect((host, port))
        cert = wrapped_sock.getpeercert(True)
        digest = hashlib.sha1(cert).hexdigest()
        # Transform deadbeaf... -> DE:AD:BE:AF:...
        return ":".join(digest[i:i + 2].upper() for i in range(0, len(digest), 2))
    finally:
        if wrapped_sock:
            wrapped_sock.close()
        else:
            sock.close()
