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
from unify.assetaccess import AssetAccess


class AssetAccessTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.access = AssetAccess(
            cluster=cluster_name,
            props=props,
            orgid=test_org
        )

    @unittest.skip("Asset Access is currently un-accessible")
    def test_get_all_tables(self):
        tables = self.access.get_all_tables()

        self.assertTrue(len(tables) > 0, tables)

    @unittest.skip("Asset Access is currently un-accessible")
    def test_execute_query(self):
        tables = self.access.get_all_tables()

        self.assertTrue(len(tables) > 0, tables)

        table = tables[0]["database"]

        results = self.access.execute_query(
            query='select * from {}'.format(table)
        )
        self.assertTrue(len(results) > 1, results)
