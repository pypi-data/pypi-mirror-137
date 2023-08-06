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
Contains methods to interact with graphs api
"""
import json

from unify.properties import Properties
from unify.properties import ClusterSetting
from unify.apirequestsmng import ApiRequestManager
from unify.helpers.SingleOrg import single_org


class Hierarchy(ApiRequestManager):
    """
    Class to interact with hierarchies endpoints
    """

    def __init__(self, cluster=None, props=Properties(ClusterSetting.KEY_RING), org_id=None):
        """
        Class constructor

        :param cluster: Cluster name to be used
        :type cluster: str
        :param props: Properties instantiated object
        :type props: class:`unify.properties.Properties`
        """
        super().__init__(cluster=cluster, props=props, org_id=org_id)

        self.session.headers.update(
            {
                self.x_auth_token_header: self.props.get_auth_token(cluster=self.cluster)
            }
        )

        remote = self.props.get_remote(self.cluster)

        self.home_hierarchies_url = remote + "api/v2/orgs/{}/asset_hierarchies"

        self.home_hierarchies_2_url = remote + "api/v2/asset_hierarchies"

        self.add_level_url = remote + "api/v2/asset_hierarchies/{}/levels"

        self.specific_hierarchy_url = remote + "api/v2/asset_hierarchies/{}"

    @single_org
    def get_all_hierarchies(self, org_id=None):
        """
        retrieve all hierarchies on the given organization

        :param org_id: organization id to be queried
        :return:
        """
        header = self.build_header(
            org_id=org_id,
            others=self.content_type_header
        )

        result = self.session.get(
            self.home_hierarchies_2_url,
            headers=header
        )

        if result.status_code == 200:
            return json.loads(result.content)

        raise Exception(repr(result.content))

    @single_org
    def create_hierarchy(self, org_id=None, *, name, levels=None, attribute_names=None, private=False):
        """
        Creates a new hierarchy with the given configuration

        :param org_id: Organization id where the hierarchy will be created
        :param name: Name for the new hierarchy, unique
        :param levels: Arrays containing the name of levels
        :param attribute_names:
        :param private:
        :return:
        """

        if levels is None:
            levels = []

        header = self.build_header(
            org_id=org_id,
            others=self.content_type_header
        )

        body = {
            "name": name,
            "levels": [],
            "assetAttributeNames": attribute_names if attribute_names is not None else [],
            "isPrivate": private,
            "draft": False
        }
        result = self.session.post(
            self.home_hierarchies_2_url,
            headers=header,
            data=json.dumps(body)
        )

        if result.status_code in [201]:
            content = json.loads(result.content)
            for level in levels:
                self.add_level(
                    org_id=org_id,
                    hierarchy_id=content["id"],
                    level_name=level
                )

            return content

        raise Exception(repr(result.content))

    @single_org
    def get_hierarchy(self, org_id=None, *, hierarchy_id):
        """
        Retrieves all the information of the given hierarchy

        :param org_id: organization id where the hierarchy is stored
        :param hierarchy_id:
        :return:
        """
        header = self.build_header(
            org_id=org_id,
            others=self.content_type_header
        )

        result = self.session.get(
            self.specific_hierarchy_url.format(hierarchy_id),
            headers=header
        )

        if result.status_code == 200:
            return json.loads(result.content)

        raise Exception(repr(result.content))

    @single_org
    def add_level(self, org_id=None, *, hierarchy_id, level_name):
        """
        Add a node level to the given hierarchy

        :param org_id: organization id where the hierarchy is stored
        :param hierarchy_id:
        :param level_name:
        :return:
        """

        header = self.build_header(
            org_id=org_id,
            others=self.content_type_header
        )

        body = {
            "groupName": level_name
        }

        result = self.session.post(
            self.add_level_url.format(hierarchy_id),
            headers=header,
            data=json.dumps(body)
        )

        if result.status_code in [201]:
            return json.loads(result.content)

        raise Exception(repr(result.content))
