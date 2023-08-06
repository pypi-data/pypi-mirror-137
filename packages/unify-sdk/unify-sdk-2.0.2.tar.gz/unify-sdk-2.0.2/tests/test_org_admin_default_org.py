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

import unittest
from tests import *


class TestOrgAdminDefaultOrg(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.org_admin = OrgAdmin(
            cluster=cluster_name,
            props=props,
            org_id=test_org
        )

    def test_get_org_info(self):
        """
        Verify the sdk can retrieve org info

        :return:
        """

        info, _ = self.org_admin.get_org_info()

        self.assertTrue("id" in info, info)
        self.assertEqual(str(info["id"]), str(test_org), info)

    def test_submit_sensor_diagnostics(self):
        info = self.org_admin.submit_sensor_diagnostics(
            content=open("tests/sensor.json", "r+").read()
        )
        self.assertTrue("reportId" in info)

    def test_create_org(self):
        org_name = "zQA-{}".format(str(uuid.uuid4()))
        create = self.org_admin.create_organization(org_name=org_name)
        self.assertTrue(
            str(create).strip().isdigit(),
            "Org Id is created and its a number"
        )

    def test_delete_org(self):
        org_name = "zQA-{}".format(str(uuid.uuid4()))
        create = self.org_admin.create_organization(org_name=org_name)

        org_admin_2 = OrgAdmin(
            cluster=cluster_name,
            props=props,
            org_id=create
        )

        delete = org_admin_2.delete_organization()

        self.assertTrue("message" in delete)

    @unittest.skip("Random passwords are hard")
    def test_invite_machine_user(self):
        invite = self.org_admin.invite_machine_user(
            id=str(uuid.uuid4()),
            password='xY+psKZ9c]5/N%,26{}'.format(str(uuid.uuid4())),
            fullname=str(uuid.uuid4()),
            role="Admin"
        )

        self.assertTrue("userId" in invite)

    def test_rename_organization(self):
        org_name = "zQA-{}".format(str(uuid.uuid4()))
        create = self.org_admin.create_organization(org_name=org_name)

        org_admin_2 = OrgAdmin(
            cluster=cluster_name,
            props=props,
            org_id=create
        )

        rename = org_admin_2.rename_organization(new_name="zQA-{}".format(str(uuid.uuid4())))

        self.assertEqual(str(rename["id"]), str(create), rename)
        self.assertTrue("name" in rename)
