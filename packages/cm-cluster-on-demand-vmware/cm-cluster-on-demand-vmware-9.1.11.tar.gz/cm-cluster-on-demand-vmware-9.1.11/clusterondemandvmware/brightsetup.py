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

import clusterondemand.brightsetup
from clusterondemand.configuration import CFG_NO_ADMIN_EMAIL, NO_WLM
from clusterondemandconfig import config

log = logging.getLogger("cluster-on-demand")


def generate_bright_setup(cluster_name, node_disk_setup_path, node_ovf):
    license_dict = clusterondemand.brightsetup.get_license_dict(cluster_name)

    admin_email = config["admin_email"] if config["admin_email"] != CFG_NO_ADMIN_EMAIL else None

    brightsetup = clusterondemand.brightsetup.generate_bright_setup(
        cloud_type="vmware",
        wlm=config["wlm"] if config["wlm"] != NO_WLM else "",
        hostname=cluster_name,
        password=config["cluster_password"],
        node_count=0,  # these are physical nodes, which we won't need here
        timezone=config["timezone"],
        admin_email=admin_email,
        license_dict=license_dict,
        node_kernel_modules=config["node_kernel_modules"],
        node_disk_setup_path=node_disk_setup_path
    )

    brightsetup["modules"]["brightsetup"]["vmware"] = {
        "cluster_name": cluster_name,
        "vmware_resource_pool": config["vmware_resource_pool"],
        "default_ovf_name": node_ovf,
        "api": {
            "host": config["vmware_address"],
            "username": config["cmd_vmware_username"] or config["vmware_username"],
            "password": config["cmd_vmware_password"] or config["vmware_password"],
            "verify_cert": config["vmware_verify_certificate"],
        },
        "network": {
            "name": cluster_name,
            "network_id": "",
            "cidr": str(config["internal_cidr"]),
            "head_node_ip": str(config["head_node_internal_ip"]),
        },
        "nodes": {
            "base_name": "cnode",
            "count": config["nodes"],
            "num_cpus": config["node_number_cpus"],
            "memory_size": config["node_memory_size"],
            "storage": {
                "root-disk": config["node_root_volume_size"],
            },
            "ovf_name": node_ovf,
            "nic": "BOOTIF",
        },
    }

    if config["internal_mtu"]:
        brightsetup["modules"]["brightsetup"]["vmware"]["internal_mtu"] = config["internal_mtu"]

    return brightsetup
