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


class TestSourcesWithOrgID(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sources = Sources(
            cluster=cluster_name,
            props=props
        )
        cls.dataset_name = 'test-{}'.format(str(uuid.uuid4()))

    def test_source_list_default_org(self):
        source_list = self.sources.get_sources(
            org_id=test_org
        )

        self.assertTrue(len(source_list) > 0, source_list)

    def test_source_was_created(self):

        try:
            created_source = self.sources.download_dataset_content(
                org_id=test_org,
                dataset_id=test_dataset["id"]
            )

            self.assertTrue(True, created_source)

        except Exception as e:

            self.assertTrue(False, e)

    def test_big_dataset(self):
        big = self.sources.upload_big_dataset(
            name=str(uuid.uuid4()),
            org_id=test_org,
            content=open("tests/data_test.csv").read()
        )
        self.assertTrue("create" in big)

    def test_create_api_dataset(self):
        api = self.sources.create_api_data_set(
            org_id=test_org,
            name=str(uuid.uuid4()),
            file_path="tests/data_test.csv"
        )

        self.assertTrue("data_set_id" in api, api)

    def test_create_api_dataset_content(self):
        api = self.sources.create_api_data_set_with_content(
            name=str(uuid.uuid4()),
            org_id=test_org,
            content=open("tests/data_test.csv").read()
        )

        self.assertTrue("data_set_id" in api, api)

    def test_commit_status(self):
        api = self.sources.create_api_data_set(
            name=str(uuid.uuid4()),
            org_id=test_org,
            file_path="tests/data_test.csv"
        )

        commit, response_code = self.sources.get_commit_status(
            org_id=test_org,
            commit_id=api["commit_id"],
            data_set_id=api["data_set_id"]
        )

        self.assertTrue(response_code in [200, 202, 201], commit)

    def test_export_dataset(self):
        export = self.sources.create_export_dataset(
            org_id=test_org,
            dataset_ids=[test_dataset["id"]]
        )

        self.assertTrue(len(export) > 0, export)

    def test_append_data(self):
        export = self.sources.add_data_to_existing_source(
            org_id=test_org,
            name=str(uuid.uuid4()),
            data_set_id=test_dataset["id"],
            file_path="tests/data_test.csv"
        )

        self.assertTrue("status" in export, export)

    def test_overwrite_dataset(self):
        export = self.sources.overwrite_dataset(
            org_id=test_org,
            data_set_id=test_dataset["id"],
            file_path="tests/data_test.csv"
        )

        self.assertTrue("truncate" in export, export)
        self.assertTrue("stage" in export, export)
        self.assertTrue("append" in export, export)

    def test_truncate_data_set(self):
        export = self.sources.truncate_data_set(
            org_id=test_org,
            data_set_id=test_dataset["id"]
        )

        self.assertTrue("commit_id" in export, export)

    def test_append_data_v2(self):
        export = self.sources.append_dataset(
            data_set_id=test_dataset["id"],
            content=open("tests/data_test.csv").read()
            ,org_id=test_org
        )

        self.assertTrue("id" in export, export)

    def test_static_file_upload(self):
        export = self.sources.static_file_upload(
            org_id=test_org,
            name=str(uuid.uuid4()),
            content="tests/data_test.csv"
        )

        self.assertTrue("id" in export, export)

    def test_delete_source(self):
        export = self.sources.static_file_upload(
            org_id=test_org,
            name=str(uuid.uuid4()),
            content="tests/data_test.csv"
        )

        delete = self.sources.delete_source(
            org_id=test_org,
            source_id=export["id"]
        )

        self.assertEqual(delete['message'], 'Success', delete)
