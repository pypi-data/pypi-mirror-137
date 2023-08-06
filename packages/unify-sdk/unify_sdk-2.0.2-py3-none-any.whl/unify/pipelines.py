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
Contains methods to interact with pipeline api
"""
import json
import uuid

from tempfile import mkstemp

from unify.generalutils import json_to_csv
from unify.properties import Properties
from unify.properties import ClusterSetting
from unify.apirequestsmng import ApiRequestManager
from unify.helpers.SingleOrg import single_org


class Pipelines(ApiRequestManager):
    """
    Class to interact with pipeline endpoints
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

        try:

            remote = self.props.get_remote(self.cluster)

            self.pipelines_url = self.props.get_remote(
                self.cluster) + "tags/org/" + '{}' + "/pipelines"

            self.regular_duplicate_url = self.pipelines_url + "/v2/{}/duplicate"

            self.delete_pipeline_url = self.pipelines_url + '/{}'

            self.pipeline_url = self.pipelines_url + '/{}'

            self.flow_url = self.pipeline_url + '/flows/{}'

            self.run_pipeline_url = self.pipeline_url + '/run'

            self.create_map_attributes_transf = self.pipeline_url + "/components/{}/map-attribute-rules"

            self.pipelines_url_v2 = self.pipelines_url + "/v2/{}"

            self.autosync_url = remote + "tags/org/{}/pipelines/{}/autosync"

            self.retrieve_pipelines_v2 = remote + "tags/org/" + '{}' + "/pipelines/v2"

            self.duplicate_pipeline_url = self.pipelines_url_v2 + "/duplicate"

            self.published_pipelines_url = remote + 'api/orgs/{}/graphs/current/pipelines'

            self.preview_data_pipeline = self.flow_url + '/preview?pageNum=1&sortKey={}&sortDir=ASC'

            self.download_map_attribute_rules = remote + 'tags/org/{}/pipelines/{}/components/{}/map-attribute-rules/csv'

            self.flow_preview_url = self.flow_url + '/preview?pageNum=1'

            self.download_flow_url = self.props.get_remote(
                self.cluster
            ) + "tags/org/{}/pipelines/{}/flows/{}/download"

            self.rules_by_templates_url = remote + "tags/org/{}/pipelines/{}/components/{}/map-attribute-rules/rules-by-template"

            self.distinct_values_map_attributes = self.props.get_remote(
                self.cluster) + "tags/org/{}/pipelines/{}/flows/{}/distinctValuesWithCount"

            self.apply_map_attributes_url = self.props.get_remote(
                self.cluster) + "tags/org/{}/pipelines/{}/components/{}/map-attribute-rules"

            self.count_endpoint = self.props.get_remote(self.cluster) + "tags/org/{}/pipelines/{}/flows/{}/count"

            self.distinct_count_values_url = self.props.get_remote(
                self.cluster) + 'tags/org/{}/pipelines/{}/flows/{}/distinctValuesWithCount'

            self.distinct_values_url = self.props.get_remote(
                self.cluster) + 'tags/org/{}/pipelines/{}/flows/{}/distinctValues'

        except Exception as error:
            raise error

    @single_org
    def apply_map_attributes(self, org_id=None, pipeline_id=None, component=None, payload=None):
        """
        Applies map attribute rules to given component

        :param org_id: Org id where the pipeline exists
        :type org_id: int or str
        :param pipeline_id: Pipeline where the map attributes component exists
        :type pipeline_id: int or str
        :param component: Map attribute component id where the rules are applied
        :type component: int or str
        :param payload: Dict representing mappings
        :type payload: dict
        :return:
        """

        final_url = self.apply_map_attributes_url.format(org_id, pipeline_id, component)

        header = self.build_header(
            org_id=org_id,
            others=self.delete_content_type_header
        )

        result = self.session.post(final_url, headers=header, data=json.dumps(payload))

        if result.status_code == 200:
            return json.loads(result.content)

        raise Exception(repr(result.content))

    @single_org
    def regular_duplicate(self, org_id=None, *, pipeline_id, new_name):
        """
        Will duplicate the given pipeline on the given org
        :param org_id:
        :param pipeline_id:
        :param new_name:
        :return:
        """
        if pipeline_id is None:
            raise Exception("Pipeline id cant be null")
        if new_name is None:
            raise Exception("New pipeline name cant be none")

        headers = self.build_header(
            org_id=org_id,
            others={"Content-Type": "application/json"}
        )

        upload_url = self.regular_duplicate_url.format(org_id, pipeline_id)

        post_upload_file = self.session.post(
            upload_url,
            headers=headers,
            data=json.dumps({"name": new_name})
        )

        if post_upload_file.status_code == 200:
            response = json.loads(post_upload_file.content)

            if "sourceMetadata" in response:
                del response["sourceMetadata"]

            return response

        raise Exception(repr(post_upload_file.content))

    @single_org
    def update_pipeline_from_json(self, org_id=None, update_payload=None, pipeline_id=None, pipeline_name=None,
                                  sources=None):
        """
        Updates a pipeline with a json content

        :param org_id: Org id where the pipeline is located
        :type org_id: int or str
        :param update_payload: JSON payload that contains pipeline content
        :type update_payload: dict
        :param pipeline_id: Pipeline identification
        :type pipeline_id: int or str
        :param pipeline_name: Pipeline current name
        :type pipeline_name: str
        :param sources: List of sources id to use
        :type sources: list of str
        :return:
        """

        header = self.build_header(
            org_id=org_id, others=self.content_type_header
        )

        update_payload["name"] = str(pipeline_name)

        index = 0

        for component in update_payload["components"]:
            if sources is not None and len(sources) > 0:
                if component["jsonClass"] == "JsonSourceRef":

                    if self.evergreen_enabled is False:
                        if "version" in component:
                            del component["version"]
                            component["sourceId"] = "100"

                    if isinstance(sources[index], int):
                        component["sourceId"] = int(sources[index])
                    else:
                        component["sourceId"] = sources[index]
                        if self.evergreen_enabled:
                            component["version"] = 1

                    index += 1
            if sources is None:
                if component["jsonClass"] == "JsonSourceRef":
                    if self.evergreen_enabled is False:
                        if "version" in component:
                            del component["version"]
                            component["sourceId"] = 1000

            if self.evergreen_enabled:
                if "version" not in component:
                    if component["jsonClass"] == "JsonSourceRef":
                        component["version"] = 1
                        component["sourceId"] = str(uuid.uuid4())

            if component["jsonClass"] == "JsonGraphSink":
                component["orgId"] = int(org_id)

        update_pipeline_request = self.session.put(
            self.pipeline_url.format(
                org_id, pipeline_id
            ),
            headers=header,
            data=json.dumps(update_payload)
        )

        if update_pipeline_request.status_code == 200:
            return json.loads(update_pipeline_request.content)

        raise Exception(repr(update_pipeline_request.content))

    @single_org
    def download_map_attributes(self, org_id=None, *, pipeline_id, component_id):
        """
        Downloads the map attributes data from the given pipeline

        :param org_id: Org id where the pipleine exists
        :type org_id: int or str
        :param pipeline_id: Pipeline id where the componentn exists
        :type pipeline_id: int or str
        :param component_id: Component where the map attributes are located
        :type component_id: int or str
        :return:
        """
        headers = self.build_header(
            org_id=org_id,
            others=self.content_type_header
        )

        download_rules = self.download_map_attribute_rules.format(
            org_id,
            pipeline_id,
            component_id
        )

        result = self.session.get(download_rules, headers=headers)

        if result.status_code == 200:
            return result.content

        raise Exception(repr(result.content))

    @single_org
    def upload_map_attributes_from_json(self, org_id=None, pipeline_id=None, component_id=None, json_data=None):
        """
        Uploads a json file to the given map attributes component

        :param org_id: Org id where the pipeline exists
        :type org_id: int or str
        :param pipeline_id: Pipeline id where to component id exists
        :type pipeline_id: int or str
        :param component_id: Map attributes component id exists
        :type component_id: int or str
        :param json_data: Contains the map attribute rules
        :type json_data: dict
        :return:
        """
        _, path = mkstemp(suffix=".csv")

        open(path, "wb").write(json_to_csv(data_array=json_data).encode())

        self.upload_map_attributes(
            org_id=org_id,
            pipeline_id=pipeline_id,
            component_id=component_id,
            csv_file=path
        )

    @single_org
    def upload_map_attributes(self, org_id=None, pipeline_id=None, component_id=None, csv_file=None):
        """
        Uploads a csv file to the given map attributes component

        :param org_id: Org id where the pipeline exists
        :type org_id: int or str
        :param pipeline_id: Pipeline id where to component id exists
        :type pipeline_id: int or str
        :param component_id: Map attributes component id exists
        :type component_id: int or str
        :param csv_file: CSV file that contains the map attribute rules
        :type csv_file: str
        :return:
        """

        headers = self.build_header(
            org_id=org_id,
            others={"'Content-Type'": "application/data"}
        )

        files = {'file': open(csv_file, "rb")}

        upload_url = self.download_map_attribute_rules.format(org_id, pipeline_id, component_id)

        post_upload_file = self.session.post(
            upload_url,
            headers=headers,
            files=files
        )

        if post_upload_file.status_code == 200:
            response = json.loads(post_upload_file.content)

            if "sourceMetadata" in response:
                del response["sourceMetadata"]

            return response

        raise Exception(repr(post_upload_file.content))

    @single_org
    def create_pipeline(self, name, org_id=None, function=False):
        """
        Creates an empty pipeline

        :param name: New pipeline name
        :type name: str
        :param org_id: Org id where the pipeline is going to be created
        :type org_id: int or str
        :param function: Defines if the pipeline is a function or not
        :type function: boolean
        :return:
        """

        header = self.build_header(
            org_id=org_id,
            others=self.content_type_header
        )

        payload = {"name": name, "components": []}

        if function:
            payload["pipelineType"] = "function"

        result = self.session.post(
            self.pipelines_url.format(org_id),
            headers=header,
            data=json.dumps(payload)
        )

        if result.status_code == 200:
            return json.loads(result.content)

        raise Exception(json.loads(result.content))

    @single_org
    def download_flow(self, org_id=None, pipeline_id=None, flow_id=None):
        """
        Downloads the flow data

        :param org_id: Org where the piprline exists
        :type org_id: int or str
        :param pipeline_id: Pipeline id where the flow exists
        :type pipeline_id: int or str
        :param flow_id: Flow id to be queried
        :type flow_id: int or str
        :return:
        """

        header = self.build_header(
            org_id=org_id,
            others=self.content_type_header
        )

        cookies = {'_gid': 'GA1.1.1649742346.1580648966'}

        schema_url = self.download_flow_url.format(org_id, pipeline_id, flow_id)

        result = self.session.get(schema_url, headers=header, cookies=cookies)

        if result.status_code == 200:
            return result.content

        raise Exception(repr(result.content))

    @single_org
    def get_pipeline(self, org_id=None, *, pipeline_id):
        """
        Retrieves pipeline json blob

        :param org_id: Org where the pipeline to be queried exists
        :type org_id: int or str
        :param pipeline_id: Pipeline id to be queried
        :type pipeline_id: int or str
        :return:
        """

        header = self.build_header(
            others=self.content_type_header
        )

        pipeline_url = self.pipeline_url.format(org_id, pipeline_id)

        result = self.session.get(pipeline_url, headers=header)

        if result.status_code == 200:
            return json.loads(result.content)

        raise Exception(repr(result.content))

    @single_org
    def delete_pipeline(self, org_id=None, *, pipeline_id):
        """
        Deletes the given pipeline
        :param org_id:
        :param pipeline_id:
        :return:
        """

        header = self.build_header(
            others=self.content_type_header,
            org_id=org_id
        )

        result = self.session.delete(
            self.pipelines_url_v2.format(org_id, pipeline_id),
            headers=header
        )

        if result.status_code in [200, 201, 202]:
            return json.loads(result.content)

        raise Exception(repr(result.content))

    @single_org
    def unpublish_pipeline(self, org_id=None, *, pipeline_id):
        """
        Unpublishes a pipeline from graph v1
        :param org_id:
        :param pipeline_id:
        :return:
        """
        header = self.build_header(
            others=self.content_type_header,
            org_id=org_id
        )

        update_payload = {"status": "draft"}

        response = self.session.put(
            self.pipelines_url_v2.format(org_id, pipeline_id),
            headers=header,
            data=json.dumps(update_payload)
        )

        if response.status_code in [200, 201, 202]:
            return json.loads(response.content)

        raise Exception(repr(response.content))

    @single_org
    def get_map_attribute_rules(self, org_id=None, *, pipeline_id, component):
        """
        Downloads map attributes rules of the given pipeline component

        :param org_id: Org where pipeline lives
        :type org_id: int or str
        :param pipeline_id: Pipeline id to be queried
        :type pipeline_id: int or str
        :param component: Map attributes id component
        :type component: int or str
        :return:
        """

        header = self.build_header(
            org_id=org_id,
            others=self.content_type_header
        )

        final_url = self.rules_by_templates_url.format(org_id, pipeline_id, component)

        result = self.session.get(final_url, headers=header)

        if result.status_code == 200:
            return json.loads(result.content)

        raise Exception(repr(result.content))

    @single_org
    def get_distinct_values_map_attributes(self, org_id=None, *, pipeline_id, flows, columns):
        """
        Retrieves distinct values from the given flow id

        :param org_id: Org id where the pipeline/flow is located
        :type org_id: int or str
        :param pipeline_id: Id of the pipeline to be queried
        :type pipeline_id: int or str
        :param flows: Flow id
        :type flows: int or str
        :param columns: Columns to used
        :type columns: list of str
        :return:
        """

        columns.append("TEMPLATE *")

        columns.append("SENSOR *")

        cols = []

        for col_name in columns:
            cols.append(('col', col_name))

        header = self.build_header(
            org_id=org_id,
            others=self.content_type_header
        )

        final_url = self.distinct_values_map_attributes.format(org_id, pipeline_id, flows)

        result = self.session.get(final_url, headers=header, params=cols)

        if result.status_code == 200:
            return json.loads(result.content)

        raise Exception(repr(result.content))

    @single_org
    def get_pipelines_v2(self, org_id=None):
        """
        Retrieves the pipeline list from the given org

        :param org_id: Org id to be queried
        :type org_id: int or str
        :return:
        """
        header = self.build_header(
            others=self.content_type_header
        )

        get_pipelines_request = self.session.get(
            self.retrieve_pipelines_v2.format(org_id),
            headers=header
        )

        if get_pipelines_request.status_code == 200:
            return json.loads(get_pipelines_request.content)

        raise Exception(repr(get_pipelines_request.content))

    @single_org
    def verify_if_pipeline_exists_and_get_id(self, org_id=None, *, pipeline_name):
        """
        Verifies that the pipeline name exists on the given org. Returns pipeline id.

        :param org_id: Org id of pipeline
        :type org_id: int or str
        :param pipeline_name: Name of pipeline
        :type pipeline_name: str
        :return:
        """

        if pipeline_name is None:
            raise Exception("New pipeline name cant be none")

        pipeline_list = self.get_pipelines_v2(org_id=org_id)

        results = {"pipeline_id": None}

        for pipe in pipeline_list["pipelineSummaries"]:
            if pipe["name"] == pipeline_name:
                existing_pipeline_id = pipe["id"]
                results.update({"pipeline_id": existing_pipeline_id})
                break

        return results

    @single_org
    def pipeline_exists(self, org_id=None, *, pipeline_name):
        """
        Verifies that the pipeline name exists on the given org

        :param org_id: Org to query if the pipeline exists
        :type org_id: int or str
        :param pipeline_name: Pipeline name to be queried
        :type pipeline_name: str
        :return:
        """
        if pipeline_name is None:
            raise Exception("New pipeline name cant be none")

        return self.verify_if_pipeline_exists_and_get_id(
            org_id=org_id,
            pipeline_name=pipeline_name
        )["pipeline_id"] is not None

    @single_org
    def update_pipeline_metadata(self, org_id=None, *, pipeline_id, name, description="", facets=None):
        """
        Method to update a pipeline's metadata
        :param org_id: org id where the pipeline is stored
        :param pipeline_id: id of the pipeline to be edited
        :param name: new pipeline name
        :param description: description to be added
        :param facets:
        :return:
        """

        headers = self.build_header(
            others=self.content_type_header,
            org_id=str(org_id)
        )

        self.get_pipeline(
            org_id=org_id,
            pipeline_id=pipeline_id
        )

        body = {
            "name": name,
            "description": description,
            "facets": [] if facets is None else facets
        }

        url = self.pipelines_url_v2.format(org_id, pipeline_id)

        response = self.session.put(
            url,
            json=body,
            headers=headers
        )

        if response.status_code in [200, 201, 202]:
            return json.loads(response.content)

        raise Exception(repr(response.content))

    @single_org
    def preview_flow(self, org_id=None, *, pipeline_id, flow_id):

        """
        Previews the given flow with default ordering
        :param org_id:
        :param pipeline_id:
        :param flow_id:
        :return:
        """

        header = self.build_header(
            others=self.content_type_header,
            org_id=str(org_id)
        )

        cookies = {'_gid': 'GA1.1.1649742346.1580648966'}

        schema_url = self.flow_preview_url.format(org_id, pipeline_id, flow_id)

        flow_data = self.session.get(
            schema_url,
            headers=header,
            cookies=cookies
        )

        if flow_data.status_code in [200, 201, 202]:
            return json.loads(flow_data.content)

        raise Exception(repr(flow_data.content))

    @single_org
    def preview_flow_by_column(self, org_id=None, *, pipeline_id, flow_id, sort_column):

        """
        Previews the given flow ordered by the column name give
        :param org_id:
        :param pipeline_id:
        :param flow_id:
        :param sort_column:
        :return:
        """

        header = self.build_header(
            others=self.content_type_header,
            org_id=str(org_id)
        )

        schema_url = self.preview_data_pipeline.format(org_id, pipeline_id, flow_id, sort_column)

        request = self.session.get(schema_url, headers=header)

        if request.status_code in [200, 201, 202]:
            return json.loads(request.content)

        raise Exception(repr(request.content))

    @single_org
    def flow_row_count(self, org_id=None, *, pipeline_id=None, flow_id=None):

        """
        Retrieves the number of rows the given flow contains
        :param org_id:
        :param pipeline_id:
        :param flow_id:
        :return:
        """

        header = self.build_header(
            others=self.content_type_header,
            org_id=str(org_id)
        )

        schema_url = self.count_endpoint.format(org_id, pipeline_id, flow_id)

        request = self.session.get(schema_url, headers=header)

        if request.status_code in [200, 201, 202]:
            return json.loads(request.content)

        raise Exception(repr(request.content))

    @single_org
    def publish_pipeline(self, org_id=None, *, pipeline_id):

        """
        Published pipeline
        :param org_id:
        :param pipeline_id:
        :return:
        """

        header = self.build_header(
            others=self.content_type_header,
            org_id=str(org_id)
        )

        run_url = self.run_pipeline_url.format(org_id, pipeline_id)

        params = [("parquet", True)]

        run_request = self.session.post(run_url, headers=header, params=params)

        if run_request.status_code in [200, 201, 202]:
            return json.loads(run_request.content)

        raise Exception(repr(run_request.content))

    @single_org
    def get_flow_distinct_values(self, org_id=None, *, pipeline_id, flow_id, col, sort_key, count=False):
        """
        Returns distinct values from a given flow, if count is true, it will return the count per distinct value
        :param org_id:
        :param pipeline_id:
        :param flow_id:
        :param col:
        :param sort_key:
        :param count:
        :return:
        """
        headers = self.build_header(
            others=self.content_type_header,
            org_id=str(org_id)
        )

        if count:
            get_distinct_vals = self.distinct_count_values_url.format(org_id, pipeline_id, flow_id)
        else:
            get_distinct_vals = self.distinct_values_url.format(org_id, pipeline_id, flow_id)

        data = [("col", col), ("sortKey", sort_key), ("sortDir", "ASC")]

        result = self.session.get(get_distinct_vals, headers=headers, params=data)

        if result.status_code in [200, 201, 202]:
            return json.loads(result.content)

        raise Exception(repr(result.content))

    @single_org
    def autosync_pipeline(self, org_id=None, *, pipeline_id, autoSyncEnabled=True):

        """
        Changes the autosync status of a pipeline
        :param org_id:
        :param pipeline_id:
        :param autoSyncEnabled:
        :return:
        """
        headers = self.build_header(
            others=self.content_type_header,
            org_id=str(org_id)
        )

        payload = {"autoSyncEnabled": autoSyncEnabled}

        post_pipeline_request = self.session.put(
            self.autosync_url.format(org_id, pipeline_id),
            headers=headers,
            data=json.dumps(payload)
        )

        if post_pipeline_request.status_code in [200, 201, 202]:
            return json.loads(post_pipeline_request.content)

        raise Exception(repr(post_pipeline_request.content))
