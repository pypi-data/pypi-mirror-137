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
from unify.graph import Graph
from unify.apimanager import ApiManager
from tests import *


class TestGraphs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.graph = Graph(cluster_name, props)
        cls.api_manager = ApiManager(cluster=cluster_name, props=props)

    def test_retrieve_graph_list_via_manager(self):

        """
        Verify if sdk can retrieve graphs list using api manager
        :return:
        """
        raised = False
        try:
            self.api_manager.graphs_list(
                org_id=test_org
            )
        except Exception as e:
            raised = True

        self.assertFalse(raised, 'Exception raised in retrieving graphs list')

    def test_retrieve_graph_list(self):

        """
        Verify if sdk can retrieve graphs list using regular client
        :return:
        """
        raised = False
        try:
            self.graph.get_graphs_list(
                org_id=test_org
            )
        except Exception as e:
            raised = True

        self.assertFalse(raised, 'Exception raised in retrieving graphs list')

    def test_query_graph(self):
        """
        Verify if the graph endpoint can be reached by the sdk
        :return:
        """
        name = str(uuid.uuid4())
        try:
            _ = self.graph.query_graph(
                org_id=test_org,
                graph=name,
                query="MATCH (n)-[r]->(g) RETURN *"
            )

        except Exception as e:

            self.assertTrue(name in str(e), e)
