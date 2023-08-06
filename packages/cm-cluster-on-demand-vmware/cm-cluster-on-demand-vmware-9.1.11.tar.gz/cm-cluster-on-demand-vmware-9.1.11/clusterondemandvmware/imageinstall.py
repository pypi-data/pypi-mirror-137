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
import os
import sys
import time
from urllib.parse import urlparse

from com.vmware.content.library import item_client

from clusterondemand import tracing
from clusterondemand.clustercreate import generate_cluster_tags
from clusterondemand.exceptions import CODException
from clusterondemand.imagerepo import RepoImageSource, imagerepo_ns
from clusterondemand.images.find import CODImage
from clusterondemand.images.utils import flatten_images
from clusterondemand.reporting_reader import ReportingReader
from clusterondemand.utils import confirm, confirm_ns
from clusterondemandconfig import ConfigNamespace, config, may_not_equal_none, requires_other_parameter_to_be_set

from . import clientutils
from .clientutils import get_server_cert_thumbprint
from .configuration import vmwarecommon_ns
from .images import findimages_ns
from .utils import print_images_table

log = logging.getLogger("cluster-on-demand")


config_ns = ConfigNamespace("vmware.image.install", help_section="image install parameters")
config_ns.import_namespace(vmwarecommon_ns)
config_ns.import_namespace(confirm_ns)
config_ns.import_namespace(findimages_ns)
config_ns.import_namespace(imagerepo_ns)
config_ns.add_parameter(
    "manifest_file",
    help="Manifest file to get image information",
)
config_ns.add_parameter(
    "url",
    help="URL to the OVA",
    validation=requires_other_parameter_to_be_set("manifest_file"),
)
config_ns.add_parameter(
    "content_library_name",
    help="Name of the content library to create the item",
    validation=may_not_equal_none,
)
config_ns.add_switch_parameter(
    "dry_run",
    flags=["-d"],
    help="Do not actually download and install",
)
config_ns.add_parameter(
    "image_file",
    flags=["-i"],
    help="Path to the OVA file"
)


def make_image_tags(cod_image):
    tags = [f"COD::{prop}={value}" for prop, value in cod_image.get_properties().items()]
    tags += [f"COD::image_tag::{tag}" for tag in cod_image.tags]
    return tags


def set_image_tags(item_id, cod_image):
    log.info("Tagging image")
    tags = make_image_tags(cod_image)
    log.debug(f"Setting image tags: {tags}")
    clientutils.get_service_manager().create_tags(tags)
    clientutils.get_service_manager().set_tags(item_id, tags)


def update_item_id_with_url(item_id, url):
    sm = clientutils.get_service_manager()

    # Create an UpdateSessionModel instance to track the changes you make to the item.
    update_session_model = item_client.UpdateSessionModel()
    update_session_model.library_item_id = item_id
    session_id = sm.vsphere.content.library.item.UpdateSession.create(create_spec=update_session_model)

    # Create a new AddSpec instance to describe the properties of the file to be uploaded.
    update_session_client = sm.vsphere.content.library.item.updatesession
    file_spec = update_session_client.File.AddSpec()
    filename = os.path.basename(urlparse(url).path)
    if not filename.endswith(".ova"):
        # WARNING: This .ova is important. Otherwise the content library doesn't know what to do with the file
        raise CODException(f"File {filename} cannot be used to create the image. It must have the 'ova' extension")

    file_spec.name = filename
    file_spec.source_type = update_session_client.File.SourceType.PULL

    # Specify the location from which the file is to be uploaded to the library item.
    endpoint = item_client.TransferEndpoint()
    endpoint.uri = url

    # If we don't set anything, our current setup at Dell will complain if we leave as None
    parsed_url = urlparse(url)
    endpoint.ssl_certificate_thumbprint = get_server_cert_thumbprint(parsed_url.hostname,
                                                                     parsed_url.port or 443)
    file_spec.source_endpoint = endpoint

    # Link the file specification to the update session.
    sm.vsphere.content.library.item.updatesession.File.add(update_session_id=session_id, file_spec=file_spec)

    # Mark session as completed, to initiate the asynchronous transfer.
    sm.vsphere.content.library.item.UpdateSession.complete(session_id)

    def report_progress(session, previous_status):
        if not sys.stderr.isatty:
            return ""
        status = f"Upload in progress: {session.client_progress}%" if session.client_progress < 100 else ""
        if status != previous_status:
            sys.stderr.write("\r" + status)

        return status

    status = ""
    while True:
        session = sm.vsphere.content.library.item.UpdateSession.get(session_id)
        status = report_progress(session, status)
        if session.state == item_client.UpdateSessionModel.State.ERROR:
            raise CODException(f"Error importing item: {session.error_message}")
        elif session.state == item_client.UpdateSessionModel.State.DONE:
            return
        time.sleep(10)

    sm.vsphere.content.library.item.UpdateSession.delete(session_id)


def update_item_id_with_local_file(item_id, file_path):
    sm = clientutils.get_service_manager()

    # Create an UpdateSessionModel instance to track the changes you make to the item.
    update_session_model = item_client.UpdateSessionModel()
    update_session_model.library_item_id = item_id
    session_id = sm.vsphere.content.library.item.UpdateSession.create(create_spec=update_session_model)

    # Create a new AddSpec instance to describe the properties of the file to be uploaded.
    update_session_client = sm.vsphere.content.library.item.updatesession
    file_spec = update_session_client.File.AddSpec()
    filename = os.path.basename(file_path)
    if not filename.endswith(".ova"):
        # WARNING: This .ova is important. Otherwise the content library doesn't know what to do with the file
        raise CODException(f"File {filename} cannot be used to create the image. It must have the 'ova' extension")

    file_spec.name = filename
    file_spec.source_type = update_session_client.File.SourceType.PUSH
    file_spec.size = os.path.getsize(file_path)

    # Link the file specification to the update session.
    file_info = sm.vsphere.content.library.item.updatesession.File.add(update_session_id=session_id,
                                                                       file_spec=file_spec)

    # Upload the file content to the file upload URL
    session = sm.create_session()
    session.headers.update({
        "Cache-Control": "no-cache",
        "Content-Length": f"{file_spec.size}",
        "Content-Type": "text/ova",
    })
    with ReportingReader(file_path, progress_prefix="Upload in progress: ") as local_file:
        req = session.post(file_info.upload_endpoint.uri, data=local_file)
        req.raise_for_status()

    # Mark session as completed
    sm.vsphere.content.library.item.UpdateSession.complete(session_id)
    sm.vsphere.content.library.item.UpdateSession.delete(session_id)


def create_cod_image_library_item(cod_image, library_name):
    if cod_image.cloud_type != "vmware":
        raise CODException(f"Cannot upload image type '{cod_image.cloud_type}' to VMWare.")

    # Create a new library item to hold the uploaded file.
    item_name = cod_image.name
    return clientutils.create_library_item(library_name, item_name, "ovf")


def create_image_from_file(cod_image, file_path, library_name):
    item_id = create_cod_image_library_item(cod_image, library_name)
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    original_size_mb = cod_image.size / (1024 * 1024)
    percentage = (file_size_mb / original_size_mb) * 100

    try:
        log.info(f"Uploading image {cod_image.name}...")
        log.info(f"File {file_path} is {percentage:.2f}% of the raw image size "
                 f"({file_size_mb:.2f}MB/{original_size_mb:.2f}MB)")
        timer = tracing.Timer()
        update_item_id_with_local_file(item_id, file_path)
        elapsed = timer.get_elapsed()
        log.info(f"Finished uploading in {elapsed:.0f} seconds ({file_size_mb / timer.get_elapsed():.2f}MB/s)")
        set_image_tags(item_id, cod_image)
        return item_id
    except Exception:
        log.error(f"Error uploading OVA. The image {cod_image.name} will be deleted")
        clientutils.get_service_manager().vsphere.content.library.Item.delete(item_id)
        raise


def create_image_from_url(cod_image, ova_url, library_name):
    item_id = create_cod_image_library_item(cod_image, library_name)

    try:
        update_item_id_with_url(item_id, ova_url)
        set_image_tags(item_id, cod_image)
        return item_id
    except Exception:
        log.error(f"Error importing OVA. The image {cod_image.name} will be deleted")
        clientutils.get_service_manager().vsphere.content.library.Item.delete(item_id)
        raise


def create_cluster_tags(image):
    cluster_tags = generate_cluster_tags(image, only_image_tags=True)
    clientutils.get_service_manager().create_tags(cluster_tags)
    # Unassociated tags are automatically cleaned up on "image delete". That can happen even if some other image is
    # being deleted. To ensure that the tags for a cluster with a certain image exist we tag the image.
    clientutils.get_service_manager().set_tags(image.uuid, cluster_tags)


def install_images_from_urls(image_url_tuples, library_name):
    print_images_table([image for image, url in image_url_tuples])
    if not confirm("About to install these images"):
        return

    for image, url in image_url_tuples:
        log.info(f"Creating image {image.name} with URL {url}")
        if config["dry_run"]:
            log.info("Image will not be installed. Dry run mode")
        elif clientutils.get_library_item_id_by_name(image.name):
            # TODO (CM-33454) Image update. On cod-os we have --update, maybe we could do something similar here
            log.info("Image already exists.")
        else:
            image.uuid = create_image_from_url(image, url, library_name)
            create_cluster_tags(image)


def install_image_from_file(image, image_file, library_name):
    image.uuid = create_image_from_file(image, image_file, library_name)
    create_cluster_tags(image)


def run_command():
    image_file = config["image_file"]
    url = config["url"]
    manifest_file = config["manifest_file"]
    library_name = config["content_library_name"]

    if image_file:
        # The config validation is taking care of this
        assert manifest_file is not None
        image = CODImage.from_manifest_file(config["manifest_file"])
        install_image_from_file(image, image_file, library_name)
    elif url:
        # The config validation is taking care of this
        assert manifest_file is not None
        image = CODImage.from_manifest_file(config["manifest_file"])
        install_images_from_urls([(image, url)], library_name)
    else:
        images = RepoImageSource.find_images_using_options(config)
        images = list(flatten_images(images))

        image_url_tuples = [
            (image, image.repo_image.url()) for image in images
        ]

        install_images_from_urls(image_url_tuples, library_name)
