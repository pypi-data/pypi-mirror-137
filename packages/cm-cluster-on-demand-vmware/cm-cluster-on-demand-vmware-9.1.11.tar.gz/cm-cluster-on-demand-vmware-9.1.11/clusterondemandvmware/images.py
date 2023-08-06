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
import re
from itertools import chain

from dateutil.parser import parse as parse_datetime

from clusterondemand.images.find import CODImage, ImageSource
from clusterondemand.images.find import findimages_ns as common_findimages_ns
from clusterondemandconfig import ConfigNamespace

from . import clientutils

log = logging.getLogger("cluster-on-demand")

findimages_ns = ConfigNamespace("vmware.images.find", help_section="image filter parameters")
findimages_ns.import_namespace(common_findimages_ns)
findimages_ns.override_imported_parameter("cloud_type", default="vmware")


class VMWareImageSource(ImageSource):
    @classmethod
    def from_config(cls, config, ids=None):
        return VMWareImageSource(
            ids=ids if ids is not None else config["ids"],
            tags=config["tags"],
            version=config["version"],
            distro=config["distro"],
            package_groups=config["package_groups"],
            revision=config["revision"],
            status=config["status"],
            advanced=config["advanced"],
            image_visibility=config["image_visibility"],
            cloud_type=config["cloud_type"],
        )

    def _iter_from_source(self):
        sm = clientutils.get_service_manager()

        # TODO Optimize search by IDs
        vmware_tags = []
        for tag in self.tags:
            vmware_tags.append(f"COD::image_tag::{tag}")

        if self.version:
            vmware_tags.append(f"COD::bcm_version={self.version}")
        if self.distro:
            vmware_tags.append(f"COD::bcm_distro={self.distro}")
        if self.distro_family:
            vmware_tags.append(f"COD::bcm_distro_family={self.distro_family}")
        if self.revision:
            vmware_tags.append(f"COD::bcm_image_revision={self.revision}")
        if self.type:
            vmware_tags.append(f"COD::bcm_image_type={self.type}")
        if self.cloud_type:
            vmware_tags.append(f"COD::bcm_cloud_type={self.cloud_type}")

        if vmware_tags:
            log.debug(f"Searching images on VMWare with tags: {vmware_tags}")
            image_ids = sm.get_objs_attached_to_tags("com.vmware.content.library.Item", vmware_tags)
        else:
            library_ids = sm.vsphere.content.Library.list()
            image_ids = chain.from_iterable(
                sm.vsphere.content.library.Item.list(library_id) for library_id in library_ids
            )

        for image_id in image_ids:
            vmware_tags = sm.get_tags(image_id)
            properties, tags = parse_vmware_tags(vmware_tags)
            if "bcm_cloud_type" not in properties:
                continue
            yield make_cod_image_from_vmware(image_id, properties, tags)


def parse_vmware_tags(vmware_tags):
    PROPERTY_RE = re.compile(r"COD::(?P<name>bcm_.*)=(?P<value>.*)")
    TAG_RE = re.compile(r"COD::image_tag::(?P<tag>.*)")

    properties = {
        match.group("name"): match.group("value")
        for tag in vmware_tags
        for match in [PROPERTY_RE.match(tag)] if match
    }

    tags = [
        match.group("tag")
        for tag in vmware_tags
        for match in [TAG_RE.match(tag)] if match
    ]

    return properties, tags


def make_cod_image_from_vmware(image_id, properties, tags):
    created_at = parse_datetime(properties.get("bcm_created_at")) if properties.get("bcm_created_at") else None
    pgs = properties.get("bcm_package_groups", "").split(",") if properties.get("bcm_package_groups") else []
    library_item = clientutils.get_service_manager().vsphere.content.library.Item.get(image_id)

    cod_image = CODImage(
        bcm_optional_info=properties.get("bcm_optional_info", ""),
        cloud_type=properties.get("bcm_cloud_type", ""),
        cluster_tools_hash=str(properties.get("bcm_cluster_tools_hash", "")),
        cmd_hash=str(properties.get("bcm_cmd_hash", "")),
        cmd_revision=int(properties.get("bcm_cmd_revision", 0)),
        cm_setup_hash=str(properties.get("bcm_cm_setup_hash", "")),
        created_at=created_at,
        distro_family=properties.get("bcm_distro_family", ""),
        distro=properties.get("bcm_distro", ""),
        id=properties.get("bcm_image_id", ""),
        image_visibility="public",
        name=library_item.name,
        package_groups=pgs,
        revision=int(properties.get("bcm_image_revision", "")),
        # TODO Fix this size to get the actual deployment size
        size=library_item.size,
        tags=tags,
        type=str(properties.get("bcm_image_type", "")),
        uploaded_at=library_item.creation_time,
        uuid=image_id,
        version=str(properties.get("bcm_version", "")),
    )
    if cod_image.created_at is None:
        cod_image.created_at = cod_image.uploaded_at
    return cod_image
