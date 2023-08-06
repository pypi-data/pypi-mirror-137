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

import requests
import urllib3
from com.vmware import nsx_policy_client
from com.vmware.nsx_policy.model_client import (
    ApiError,
    Segment,
    SegmentSecurityProfile,
    SegmentSecurityProfileBindingMap
)
from com.vmware.vapi.std.errors_client import Error as ClientError
from tenacity import retry, retry_if_exception_type, stop_after_delay, wait_fixed
from vmware.vapi.bindings.stub import ApiClient
from vmware.vapi.lib import connect
from vmware.vapi.stdlib.client.factories import StubConfigurationFactory

from clusterondemandconfig import config

log = logging.getLogger("cluster-on-demand")


class SegmentExistsError(Exception):
    def __init__(self, name):
        message = f"Segment '{name}' already exists."
        super().__init__(message)


class TransportZoneDoesNotExistError(Exception):
    def __init__(self, transport_zone_id):
        message = f"Transport Zone '{transport_zone_id}' does not exist."
        super().__init__(message)


class SecurityProfileDoesNotExistError(Exception):
    def __init__(self, security_profile_id):
        message = f"Security profile with id '{security_profile_id}' does not exist."
        super().__init__(message)


class NsxApiError(Exception):
    pass


class RetryableNsxApiError(Exception):
    pass


class NsxClient(object):
    """
    Client to use the NSX-T REST API in Policy mode.
    """

    def __init__(self):
        """
        Create a NSX-T client that uses session based authentication.
        """
        stub_config = NsxClient._create_stub_config()
        api_stub = nsx_policy_client.StubFactory(stub_config)
        self._client = ApiClient(api_stub)

    def create_internalnet_security_profile(self, name):
        """
        Create a security profile for the internal network.

        Because we run a DHCP server on the headnode we need to allow ipv4 DHCP traffic.
        For all other fields we fall back to the default settings.
        """
        security_profile_id = name
        security_profile = SegmentSecurityProfile(id=security_profile_id,
                                                  dhcp_server_block_enabled=False,
                                                  dhcp_client_block_enabled=False)
        try:
            profile = self._client.infra.SegmentSecurityProfiles.update(security_profile_id, security_profile)
        except ClientError as error:
            parsed_error = error.data.convert_to(ApiError)
            raise NsxApiError(parsed_error.error_message)

        return profile

    def create_internalnet_segment(self, name, transport_zone_id, security_profile_id):
        """
        Create a network segment for the internal network of a COD cluster.

        This network segment will be deployed as a standalone segment that uses the provided security profile.
        If this security profile does not exist, we create a new security profile that allows DHCP traffic.
        """
        if self._segment_exists(name):
            raise SegmentExistsError(name)

        if not self.security_profile_exists(security_profile_id):
            raise SecurityProfileDoesNotExistError(security_profile_id)

        try:
            transport_zone_path = self._get_transport_zone_path(transport_zone_id)
            segment = Segment(id=name, transport_zone_path=transport_zone_path)
            segment = self._client.infra.Segments.update(name, segment)
            self._set_segment_security_profile(segment.id, security_profile_id)
        except ClientError as error:
            parsed_error = error.data.convert_to(ApiError)
            raise NsxApiError(parsed_error.error_message)

        return segment

    @retry(retry=retry_if_exception_type(RetryableNsxApiError),
           stop=stop_after_delay(120),
           wait=wait_fixed(5),
           reraise=True)
    def delete_segment(self, segment_id):
        # Before we can delete a segment we need to break the dependency with the security profile.
        self._remove_security_profile(segment_id)

        # It can take a while before NSX is aware that the VMs are disconnected and deleted.
        # This means that NSX can temporarily fail to delete the segment because there are still VMs connected.
        # In case of this error, code 503040, we retry for 2 minutes.
        try:
            self._client.infra.Segments.delete(segment_id)
        except ClientError as error:
            parsed_error = error.data.convert_to(ApiError)
            if parsed_error.error_code == 503040:
                raise RetryableNsxApiError(parsed_error.error_message)
            else:
                raise NsxApiError(parsed_error.error_message)

    def security_profile_exists(self, profile_id):
        for profile in NsxClient._get_all_pages(self._client.infra.SegmentSecurityProfiles.list):
            if profile.id == profile_id:
                return True

        return False

    def _get_transport_zone_path(self, transport_zone_id):
        kwargs = {"site_id": "default", "enforcementpoint_id": "default"}
        fn_list_transport_zones = self._client.infra.sites.enforcement_points.TransportZones.list
        for transport_zone in NsxClient._get_all_pages(fn_list_transport_zones, **kwargs):
            if transport_zone.id == transport_zone_id:
                return transport_zone.path

        raise TransportZoneDoesNotExistError(transport_zone_id)

    def _segment_exists(self, segment_name):
        for segment in NsxClient._get_all_pages(self._client.infra.Segments.list):
            if segment.display_name == segment_name:
                return True

        return False

    def _set_segment_security_profile(self, segment_id, security_profile_id):
        """Create a security binding map for the segment using the custom profile."""
        map_id = self._get_security_map_id(segment_id)
        security_binding_map = SegmentSecurityProfileBindingMap(
            id=map_id,
            segment_security_profile_path=f"/infra/segment-security-profiles/{security_profile_id}"
        )
        self._client.infra.segments.SegmentSecurityProfileBindingMaps.update(segment_id, map_id, security_binding_map)

    def _remove_security_profile(self, segment_id):
        """Remove a security profile from the segment by deleting the security profile"""
        map_id = self._get_security_map_id(segment_id)
        self._client.infra.segments.SegmentSecurityProfileBindingMaps.delete(segment_id, map_id)

    def _get_security_map_id(self, segment_id):
        return f"{segment_id}-security-binding-map"

    @staticmethod
    def _create_stub_config():
        """
        Prepare a session based connector for the API client stub.

        VMware uses session cookies for session-based authentication.
        Session state is local to the server responding to the API request.
        Idle sessions will automatically time-out.
        """
        nsx_url = f"https://{config['nsx_address']}"
        session = requests.session()

        if not config["vmware_verify_certificate"]:
            session.verify = config["vmware_verify_certificate"]
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # For authentication we need to set an authentication cookie and X-XSRF-TOKEN header.
        # We can retrieve the cookie and X-XSRF-TOKEN from the NSX-T API.
        payload = {"j_username": config["nsx_username"], "j_password": config["nsx_password"]}
        response = session.post(f"{nsx_url}/api/session/create", data=payload)
        response.raise_for_status()
        session.headers["Cookie"] = response.headers.get("Set-Cookie")
        session.headers["X-XSRF-TOKEN"] = response.headers.get("X-XSRF-TOKEN")

        connector = connect.get_requests_connector(session=session, msg_protocol="rest", url=nsx_url)
        return StubConfigurationFactory.new_runtime_configuration(connector, response_extractor=True)

    @staticmethod
    def _get_all_pages(function, **kwargs):
        """
        Iterate over all pages of a VMware API list call.

        Any paged API endpoint can be used, to pass arguments to the calls use the keyword arguments.
        For example, to iterate over all security profiles with a page size of 10:

            for result in _get_all_pages(self._api_client.infra.SegmentSecurityProfiles.list, page_size=10):
        """
        current_page = function(**kwargs)

        while(True):
            for result in current_page.results:
                yield result

            if current_page.cursor:
                current_page = function(cursor=current_page.cursor, **kwargs)
            else:
                break
