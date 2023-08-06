# Copyright 2021 Element Analytics, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Contains general class to inherit from when creating a new api
client service
"""
import time

import json
import requests


class ApiRequestManager:
    """
    Class to interact with general api request methods
    """

    def __init__(self, cluster, props, org_id=None):
        """
        Class constructor

        :param cluster: Cluster name to interact with
        :type cluster: str
        :param props: Instantiated Properties from unify/properties
        :type props: class:`unify.properties.Properties`
        """
        self.props = props
        self.session = requests.Session()
        self.content_type_header = {"content-type": "application/json"}
        self.content_octet = {"content-type": "application/octet-stream"}
        self.upload_content_type_header = {"Content-Type": "multipart/form-data"}
        self.delete_content_type_header = {"Content-Type": "application/json"}

        self.list_templates_uri = 'api/assetTemplates'

        self.x_auth_token_header = "x-auth-token"
        self.x_org_header = "x-organization-id"
        self.cluster = cluster
        self.evergreen_enabled = True

        self.epoch_time = int(time.time())
        self.pi_tag_export_limit = {"piTagExportLimit": 999}
        self.expiry = {"expiry": 999}

        self.org_id = org_id

        auth = self.props.get_auth_token(cluster=self.cluster)

        self.api_session_url = self.props.get_remote(cluster=self.cluster) + 'api/sessions'

        if auth is None or len(auth) == 0:
            self.props.set_auth_token(
                token=self.auth_token(),
                cluster=self.cluster
            )

        self.session.headers.update(
            {
                self.x_auth_token_header: self.props.get_auth_token(cluster=self.cluster)
            }
        )

    def close_session(self):
        """
        Closes request session

        :return:
        """
        self.session.close()

    def verify_auth_token(self, cluster_name):
        """
        Verifies if the auth token is set

        :return:
        """
        if self.props.get_auth_token(cluster=cluster_name) is None:
            raise Exception(
                "Authentication is required with remote server, login running ah login"
            )

    def verify_remote(self, cluster_name):
        """
        Verifies if the remote cluster is set

        :return:
        """
        if self.props.get_remote(cluster=cluster_name) is None:
            raise Exception(
                "Remote server must be setup first"
            )

    def verify_properties(self, cluster_name):
        """
        Verify both auth token and remote cluster

        :return:
        """
        self.verify_auth_token(cluster_name=cluster_name)
        self.verify_remote(cluster_name=cluster_name)

    def auth_token(self, query_params={}):
        """
        Authenticates the given credentials and retrieves auth token

        :return:
        """

        username = self.props.get_username(cluster=self.cluster)
        password = self.props.get_password(cluster=self.cluster)

        try:
            data = {"email": username, "password": password}

            post_response = self.session.post(
                self.api_session_url,
                headers=self.content_type_header,
                data=json.dumps(data),
                params=query_params
            )

            if post_response.status_code == 200:
                return json.loads(post_response.content)["authToken"]

            raise Exception(post_response.content)

        except Exception as error:

            raise error

    def build_header(self, aut_token=None, org_id=None, others=None):
        """
        Creates request header

        :param aut_token: x-auth-token to be included
        :type aut_token: str
        :param org_id: Org id where the request will be aimed
        :type org_id: int or str
        :param others: Other headers to be included.
        :type others: dict
        :return:
        """
        header = {}

        if others is not None and isinstance(others, dict):
            header.update(others)

        if aut_token is not None:
            header[self.x_auth_token_header] = aut_token

        if org_id is not None:
            header[self.x_org_header] = str(org_id)

        return header

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
