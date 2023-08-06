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
from unify.apimanager import ApiManager


class ApiManagerDefaultOrg(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_manger = ApiManager(
            cluster=cluster_name,
            props=props
        )

        cls.test_here = sources.static_file_upload(
            name=str(uuid.uuid4()),
            org_id=test_org,
            content="tests/data_test.csv"
        )

    def test_delete_source(self):
        delete = self.api_manger.delete_source(
            org_id=test_org,
            source_id=self.test_here["id"]
        )

        self.assertTrue("message" in delete)
        self.assertEqual(delete["message"], "Success", delete)

    def test_graphs_list(self):
        graph_list = self.api_manger.graphs_list(org_id=test_org, )
        self.assertTrue(len(graph_list) is 0, graph_list)

    def test_regular_pipeline_duplicate(self):
        dupli = self.api_manger.regular_pipeline_duplicate(
            org_id=test_org,
            pipeline_id=test_pipeline["pipeline"]["id"],
            new_name=str(uuid.uuid4())
        )
        self.assertTrue("id" in dupli, dupli)

    def test_export_source(self):
        export = json.loads(self.api_manger.export_source(
            org_id=test_org,
            dataset_ids=[test_dataset["id"]]
        ))
        self.assertTrue(len(export) > 0, export)
        self.assertTrue("file_content" in export[0], export[0])

    def test_dataset_list(self):
        export = self.api_manger.dataset_list(org_id=test_org)
        self.assertTrue(len(export) > 0, export)

    def test_pipeline_list(self):
        export = self.api_manger.pipeline_list(org_id=test_org)
        self.assertTrue(len(export) > 0, export)

    def test_create_pipeline_export_data(self):
        export = self.api_manger.create_pipeline_export_data(
            org_id=test_org,
            pipeline_id=test_pipeline["pipeline"]["id"],
            skip=[]
        )

        self.assertTrue("map_attributes" in export, export)
        self.assertTrue("functions" in export, export)
        self.assertTrue("pipeline" in export, export)
        self.assertTrue("sources" in export, export)
        self.assertTrue("templates" in export, export)

    def test_proceses_importing_pipeline_file(self):
        export = self.api_manger.create_pipeline_export_data(
            org_id=test_org,
            pipeline_id=test_pipeline["pipeline"]["id"],
            skip=[]
        )
        import_results = json.loads(self.api_manger.proceses_importing_pipeline_file(
            org_id=test_org,
            content=export,
            skip=[]
        ))

        self.assertTrue("pipeline_id" in import_results, import_results)
        self.assertEqual(import_results["org_id"], test_org, import_results)
        self.assertTrue("url" in import_results, import_results)
        self.assertTrue("warnings" in import_results, import_results)

    def test_get_all_hierarchies_display(self):
        export = self.api_manger.get_all_hierarchies_display(org_id=test_org)

        self.assertTrue(len(export) > 0, export)

    def test_get_single_hierarchy(self):
        export = self.api_manger.get_all_hierarchies(org_id=test_org)

        self.assertTrue(len(export) > 0, export)

    def test_create_hierarchy(self):
        export = self.api_manger.create_hierarchy(
            org_id=test_org,
            name=str(uuid.uuid4())
        )

        self.assertTrue("id" in export, export)

    def test_export_hierarchy(self):
        export = json.loads(self.api_manger.export_hierarchy(org_id=test_org, hierarchy=test_hierarchy["id"]))

        self.assertEqual(export["name"], test_hierarchy["name"], export)
        self.assertTrue("levels" in export)

    def test_import_hierarchy(self):
        fi = json.loads(
            self.api_manger.export_hierarchy(
                org_id=test_org,
                hierarchy=test_hierarchy["id"]
            )
        )

        fi["name"] = str(uuid.uuid4())

        import_results = self.api_manger.import_hierarchy(
            org_id=test_org,
            content=json.dumps(fi),
        )

        self.assertTrue("id" in import_results, import_results)
