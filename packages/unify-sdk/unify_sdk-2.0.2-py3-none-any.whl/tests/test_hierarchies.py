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
import json

from tests import *
from unify.hierarchies import Hierarchy


class HierrachiesOrgId(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.hierarchy_mng = Hierarchy(
            cluster=cluster_name,
            props=props,
            org_id=test_org
        )

    def test_get_all_hierarchies_display(self):
        export = self.hierarchy_mng.get_all_hierarchies(org_id=test_org)

        self.assertTrue(len(export) > 0, export)

    def test_create_hierarchy(self):
        export = self.hierarchy_mng.create_hierarchy(
            org_id=test_org,
            name=str(uuid.uuid4()),
            levels=[]
        )

        self.assertTrue("id" in export, export)

    def test_get_hierarchy(self):
        fi = self.hierarchy_mng.get_hierarchy(
                org_id=test_org,
                hierarchy_id=test_hierarchy["id"]
            )

        self.assertTrue("config" in fi, fi)
        self.assertTrue("id" in fi["config"], fi)

    def test_add_level(self):

        fi = self.hierarchy_mng.add_level(
                org_id=test_org,
                hierarchy_id=test_hierarchy["id"],
                level_name=str(uuid.uuid4())
            )

        self.assertTrue("groupName" in fi, fi)
