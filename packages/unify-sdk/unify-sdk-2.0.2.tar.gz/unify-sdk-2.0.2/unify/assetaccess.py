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
Contains methods to interact with Unify access
"""

import time
from urllib.parse import urlparse
import pkg_resources
from unify.apirequestsmng import ApiRequestManager
from unify.helpers import staticsql


class AssetAccess(ApiRequestManager):
    """
    Class to interact with Unify access api client
    """

    def __init__(self, cluster, orgid, props):
        """
        Unify access api client class constructor

        :param cluster: Cluster name
        :type cluster: str
        :param orgid: Organization id
        :type orgid: int or str
        """
        super().__init__(cluster=cluster, props=props, org_id=orgid)

        required = {'psycopg2-binary'}
        installed = {pkg.key for pkg in pkg_resources.working_set}
        missing = required - installed

        if 'psycopg2-binary' in missing:
            raise Exception(
                "Please install {} by running pip install psycopg2-binary".format(
                    missing
                )
            )

        self.epoch_time = int(time.time())

        self.pi_tag_export_limit = {"piTagExportLimit": 999}

        self.expiry = {"expiry": 999}

        self.org_id = orgid

        result = urlparse(self.props.get_remote(cluster=self.cluster))

        self.connect_string = "host='{}' dbname='asset_hub_{}' port=8888 sslmode='require' user='{}' password='{}'".format(
            result.netloc,
            orgid,
            self.props.get_username(cluster),
            self.props.get_password(cluster)
        )

    def execute_query(self, query):
        """
        Creates a connection to Unify Access and executes the given query

        :param query: SQL query
        :type query: str
        :return:
        """
        required = {'psycopg2-binary'}
        installed = {pkg.key for pkg in pkg_resources.working_set}
        missing = required - installed

        if 'psycopg2-binary' in missing:
            raise Exception(
                "Please install {} by running pip install psycopg2-binary".format(
                    missing
                )
            )

        import psycopg2 as pg

        connection = pg.connect(self.connect_string)
        cursor = connection.cursor()

        cursor.execute(query=query)
        records = cursor.fetchall()
        output = []
        colnames = [desc[0] for desc in cursor.description]
        for record in records:
            aux = {}
            index = 0
            for desc in colnames:
                aux[desc] = record[index]
                index += 1

            output.append(aux)

        connection.close()

        return output

    def get_all_tables(self):
        """
        Retrieves all the tables that exists in org

        :return:
        """
        oid = self.execute_query(query=staticsql.OID_QUERY.format(self.org_id))

        if len(oid) < 1:
            raise Exception("No usable databases/datasets found for this org")

        return self.execute_query(query=staticsql.ALL_TABLES.format(oid[0]['oid']))
