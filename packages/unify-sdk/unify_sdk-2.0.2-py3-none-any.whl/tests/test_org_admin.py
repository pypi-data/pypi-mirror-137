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
This script contains some test cases for organization administration for the SDK
"""
import unittest
import os
import uuid

from tests import *


# from unify.orgadmin import OrgAdmin
# from unify.properties import Properties
# from unify.properties import ClusterSetting


class TestOrgAdmin(unittest.TestCase):

    def test_can_login(self):
        """
        Verify sdk can login
        :return:
        """
        with Properties(clusterSetting=ClusterSetting.MEMORY) as props:
            cluster_name = "qa"

            props.store_cluster(
                username=os.environ.get("username"),
                password=os.environ.get("password"),
                name=cluster_name,
                cluster=os.environ.get("cluster")
            )
            with OrgAdmin(props=props, cluster=cluster_name) as org_admin:
                token = props.get_auth_token(cluster=cluster_name)

                org_admin.close_session()

                self.assertNotEqual(token, None, "Token is None")

    def test_can_create_org(self):
        """
        Verify sdk can create org
        :return:
        """
        with Properties(clusterSetting=ClusterSetting.MEMORY) as props:
            cluster_name = "qa"

            props.store_cluster(
                username=os.environ.get("username"),
                password=os.environ.get("password"),
                name=cluster_name,
                cluster=os.environ.get("cluster")
            )

            with OrgAdmin(props=props, cluster=cluster_name) as org_admin:
                org_id = org_admin.create_organization(
                    org_name="sdk-tests-{}".format(str(uuid.uuid4()))
                )

                org_admin.close_session()

                self.assertTrue(
                    str(org_id).strip().isdigit(),
                    "Org Id is created and its a number"
                )

    def test_get_org_info(self):
        """
        Verify sdk can get org info
        :return:
        """
        with Properties(clusterSetting=ClusterSetting.MEMORY) as props:
            cluster_name = "qa"

            props.store_cluster(
                username=os.environ.get("username"),
                password=os.environ.get("password"),
                name=cluster_name,
                cluster=os.environ.get("cluster")
            )

            with OrgAdmin(props=props, cluster=cluster_name) as org_admin:
                org_id, _ = org_admin.get_org_info(
                    org_id=test_org
                )

                org_admin.close_session()

                self.assertTrue("id" in org_id, org_id)
                self.assertEqual(str(org_id["id"]), str(test_org), org_id)


if __name__ == '__main__':
    unittest.main()
