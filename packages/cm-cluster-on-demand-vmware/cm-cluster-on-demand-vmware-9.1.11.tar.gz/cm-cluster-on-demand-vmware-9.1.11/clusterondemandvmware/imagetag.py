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

from __future__ import absolute_import, print_function

import logging

from clusterondemand.exceptions import CODException
from clusterondemand.images.utils import flatten_images
from clusterondemand.utils import confirm, confirm_ns
from clusterondemandconfig import ConfigNamespace, config

from . import clientutils
from .configuration import vmwarecommon_ns
from .images import VMWareImageSource, findimages_ns
from .utils import print_images_table

log = logging.getLogger("cluster-on-demand")


config_ns = ConfigNamespace("vmware.image.tag", help_section="image tagging parameters")
config_ns.import_namespace(vmwarecommon_ns)
config_ns.import_namespace(findimages_ns)
config_ns.import_namespace(confirm_ns)
config_ns.add_enumeration_parameter(
    "add_tags",
    default=[],
    help="List of tag(s) to be added to the image(s)",
)
config_ns.add_enumeration_parameter(
    "delete_tags",
    default=[],
    help="List of tag(s) to be deleted from the image(s)",
)


def run_command():
    add_tags = set(config["add_tags"])
    delete_tags = set(config["delete_tags"])

    if set.intersection(add_tags, delete_tags):
        raise CODException("The same tags cannot be used in --add-tags and --delete-tags")

    if not config.is_item_set_explicitly("tags") and config["tags"]:
        log.warning(f"Ignoring 'tags' value from the environment: {config['tags']}. Please set explicitly if needed.")
        config["tags"] = []

    log.info("Please wait...")
    images = VMWareImageSource.find_images_using_options(config)
    images = list(flatten_images(images))

    log.info(f"The following images will be tagged:")
    print_images_table(images)
    if not confirm("About to tag these images"):
        return

    for image in images:
        log.info(f"Tagging image {image.name}")
        tags_to_add = [f"COD::image_tag::{tag}" for tag in add_tags if tag not in image.tags]
        tags_to_delete = [f"COD::image_tag::{tag}" for tag in delete_tags if tag in image.tags]

        sm = clientutils.get_service_manager()
        sm.create_tags(tags_to_add)
        sm.set_tags(image.uuid, tags_to_add)
        sm.unset_tags(image.uuid, tags_to_delete)
