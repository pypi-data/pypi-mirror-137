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
Contains methods to interact with templates api
"""
import json
import os

from unify.properties import Properties
from unify.properties import ClusterSetting
from unify.apirequestsmng import ApiRequestManager
from unify.generalutils import csv_to_json
from unify.helpers.SingleOrg import single_org


class Templates(ApiRequestManager):
    """
    Template client class to interact with templates endpoints
    """

    def __init__(self, cluster=None, props=Properties(ClusterSetting.KEY_RING), org_id=None):
        """
        Template constructor

        :param cluster: Cluster name to interact with
        :type cluster: str
        :param props: Instantiated Properties class
        :type props: class:`unify.properties.Properties`
        """
        super().__init__(cluster=cluster, props=props, org_id=org_id)

        try:

            self.list_templates_uri = 'api/assetTemplates'

            self.upload_content_type = 'text/tab-separated-values'

            self.template_list_url = "api/template_management/v1/orgs/{}/templates"

            self.delete_template_uri = 'api/template_management/v1/templates/{}'

            self.root_templete_url = self.props.get_remote(
                self.cluster) + self.list_templates_uri

            self.upload_endpoint = self.props.get_remote(
                self.cluster) + 'api/template_management/v1/templates/upload'

            self.upload_parameters_endpoint = self.props.get_remote(
                self.cluster) + 'template_management/v1/orgs/{}/templates/metadata/upload'

            self.get_sensors_uri = self.root_templete_url + "/{}/sensors"

            self.template_download_url = self.props.get_remote(
                self.cluster) + "api/template_management/v1/templates/download"

            self.template_batch_url = self.props.get_remote(
                self.cluster) + 'api/template_management/v1/orgs/{}/templates/batch'

            self.template_sensor_coverage_uri = self.props.get_remote(
                self.cluster) + "api/template_management/v1/templates/sensor-coverage"

            self.template_url = self.props.get_remote(
                self.cluster) + 'api/template_management/v1/templates'

            self.template_attribute = self.props.get_remote(
                self.cluster) + 'api/template_management/v1/orgs/{}/templates/{}/attributes'

            self.template_attribute_url = self.props.get_remote(
                self.cluster) + 'api/template_management/v1/orgs/{}/templates/{}/attributes/{}'

            self.categories_url = self.props.get_remote(
                self.cluster) + 'api/template_management/v1/orgs/{}/categories'

        except Exception as error:
            raise error

    @single_org
    def upload_template(self, file_path, org_id=None):
        """
        Uploads the given file path with templates data.

        :param file_path: File directory path with the templates contents
        :type file_path: str
        :param org_id: Org id where templates are going to be saved
        :type org_id: int or str
        :return: Upload template status message
        """

        if os.path.exists(file_path):
            file_upload = {'file': open(file_path, 'r+')}
        else:
            file_upload = {'file': file_path}

        upload_headers = self.build_header(
            org_id=org_id
        )

        post_upload_template = self.session.post(
            self.upload_endpoint,
            headers=upload_headers,
            files=file_upload
        )

        if post_upload_template.status_code == 201:
            return json.loads(post_upload_template.content)

        raise Exception(post_upload_template.content)

    @single_org
    def get_attributes(self, org_id=None, template_id=None):
        """
        Downloads all the attributes of the given template id.

        :param org_id: Org where the templates are stored
        :type org_id: int or str
        :param template_id: Template id which attributes are being downloaded
        :type template_id: int or str
        :return: Retrieve attributes status message
        """
        final_url = self.template_attribute.format(org_id, template_id)

        upload_headers = self.build_header(
            org_id=org_id
        )

        get_attrs = self.session.get(
            final_url,
            headers=upload_headers,
            params=[("pageSize", 2000)]
        )

        if get_attrs.status_code == 200:
            return json.loads(get_attrs.content)

        raise Exception(repr(get_attrs.content))

    @single_org
    def upload_string_content_file(self, org_id=None, content=None):
        """
        Uploads templates data that are stored in the variable content.

        :param org_id: Org id where templates are going to be stored
        :type org_id: int or str
        :param content: Templates contents
        :type content: str
        :return: Upload template status message
        """

        files = {'file': ('templates_uploads.csv', content, self.upload_content_type)}

        upload_headers = self.build_header(
            org_id=org_id
        )

        post_upload_template = self.session.post(
            self.upload_endpoint,
            headers=upload_headers,
            files=files
        )

        if post_upload_template.status_code == 201:
            return json.loads(post_upload_template.content)

        raise Exception(post_upload_template.content)

    @single_org
    def upload_config(self, org_id=None, file_path=None):
        """
        Uploads template configuration file.

        :param org_id: Org where the config will be applied
        :type org_id: int or str
        :param file_path: Directory file path where the contest are
        :type file_path: str
        :return: Upload template configuration status message
        """
        try:

            file_reader = open(file_path, "r+")
            try:
                content = file_reader.read()

            except Exception as e:
                file_reader.close()
                raise Exception(str(e))
            finally:
                file_reader.close()
        except FileNotFoundError:
            raise FileNotFoundError("File {} does not exist".format(file_path))

        return self.upload_config_with_content(org_id, content)

    @single_org
    def upload_config_with_content(self, org_id=None, content=None, format="csv"):
        """
        Uploads template configuration from content of a variable and not a file.

        :param org_id: Org where the templates are stored
        :type org_id: int or str
        :param content: Template config content
        :type content: str
        :param format: CSV or TSV
        :type format: str, optional
        :return: Upload template attribute configuration message
        """

        files = {
            'file': (
                f'templates_uploads.{format}',
                content,
                self.upload_content_type
            )
        }

        upload_headers = self.build_header(
            org_id=org_id
        )

        post_upload_template = self.session.post(
            self.upload_parameters_endpoint.format(org_id),
            headers=upload_headers,
            files=files
        )

        if post_upload_template.status_code == 200:
            return json.loads(post_upload_template.content)

        raise Exception(post_upload_template.content)

    @single_org
    def _add_category(self, org_id=None, category=None):
        url = self.categories_url.format(org_id)
        headers = self.build_header(
            org_id=org_id,
            others=self.content_type_header
        )
        payload = {
            "label": category,
        }

        request = self.session.post(
            url,
            headers=headers,
            data=json.dumps(payload),
        )
        if request.status_code == 200:
            return json.loads(request.content)
        raise Exception(request.content)

    @single_org
    def list_all_categories(self, org_id=None):
        """
        Retrieves all the template categories on the given org.

        :param org_id: Org id to be queried
        :type org_id: int or str
        :return: List of template categories
        """
        headers = self.build_header(
            org_id=org_id,
        )
        request = self.session.get(
            self.categories_url.format(org_id),
            headers=headers
        )
        if request.status_code == 200:
            entries = json.loads(request.content)['entries']
            entries_dic = {}
            for entry in entries:
                label = entry['label']
                entries_dic.update({label: entry['id']})
            return entries_dic
        raise Exception(request.content)

    @single_org
    def category(self, org_id=None, *, template_id, template_name, version, categories):
        """
        Updates template categories

        :param org_id: Org where the templates are stored
        :type org_id: int or str
        :param template_id: Template id
        :type template_id: int or str
        :param template_name: Template name
        :type template_name: str
        :param version: Template version
        :type version: int
        :param categories: List contains the templates categories
        :type categories: list or str
        :return: Update categories status message
        """
        existing = self.list_all_categories(org_id)
        ids = []
        for cat in categories:
            if cat in existing:
                ids.append(existing.get(cat))
            else:
                _id = self._add_category(org_id, cat)['id']
                ids.append(_id)

        url = '{}/{}?version={}'.format(self.template_url, template_id, version)
        headers = self.build_header(
            org_id=org_id,
            others=self.content_type_header
        )
        payload = {
            "organizationId": org_id,
            "name": template_name,
            "categoryIds": ids
        }

        request = self.session.put(
            url,
            headers=headers,
            data=json.dumps(payload),
            params=[("version", version)]
        )
        if request.status_code == 200:
            return json.loads(request.content)

        raise Exception(request.content)

    @single_org
    def get_template(self, org_id=None, *, template_id):
        """
        Retrieves template by id.

        :param org_id: Org id of whom templates are being retrieved
        :type org_id: int or str
        :param template_id: Template id
        :type template_id: int or str
        :return: Retrieved template str
        """
        header = self.build_header(
            org_id=org_id
        )
        url = self.template_url + '/' + str(template_id)
        request = self.session.get(url, headers=header)

        if request.status_code == 200:
            return json.loads(request.content)

        raise Exception(json.loads(request.content))

    @single_org
    def list_asset_templates(self, org_id=None):
        """
        Retrieves the templates list from the given org.

        :param org_id: Org id of whom templates are being retrieved
        :type org_id: int or str
        :return: List of templates
        """

        header = self.build_header(
            org_id=org_id
        )

        list_request = self.session.get(self.root_templete_url, headers=header)

        if list_request.status_code == 200:
            return json.loads(list_request.content)["items"]

        raise Exception(json.loads(list_request.content))

    @single_org
    def download_template(self, org_id=None, list_templates=None):
        """
        Downloads the templates data.

        :param org_id: Org where the templates exists
        :type org_id: int or str
        :param list_templates: List containing the template ids
        :type list_templates: list of str
        :return: Text representing templates
        """

        if list_templates is None:
            list_templates = []
        list_templates = list_templates if list_templates is not None else []

        header = self.build_header(
            org_id=org_id,
            others=self.content_type_header
        )

        data = tuple(["templateId", name] for name in list_templates)

        get_response = self.session.get(self.template_download_url, headers=header, params=data)

        if get_response.status_code == 200:
            return get_response.content

        raise Exception(json.loads(get_response.content))

    @single_org
    def download_all_templates(self, org_id=None, format="csv"):
        """
        Retrieves all the templates data.

        :param org_id: Org where the templates are stored
        :type org_id: int or str
        :param format: File format. Accepts "CSV" or "JSON"
        :type format: str, optional
        :return: Text representing templates
        """
        try:
            template_list_resp = self.list_asset_templates(org_id=org_id)

            template_list = [template["id"] for template in template_list_resp]

            data = self.download_template(org_id=org_id, list_templates=template_list)

            if format == "csv":
                return data

            return json.dumps(csv_to_json(csv_data=data))

        except Exception as error:
            raise error

    @single_org
    def download_all_template_config(self, org_id=None):
        """
        Retrieves all template configurations.

        :param org_id: Org where the templates are stored
        :type org_id: int or str
        :return: Text representing template metadata
        """
        try:

            header = self.build_header(
                org_id=org_id
            )

            url = self.template_batch_url.format(org_id)

            response = self.session.get(url, headers=header)

            if response.status_code not in [200, 201]:
                raise Exception(response.content)

            config_array = [["template", "attribute", "key", "value"]]

            template_sets = response.json()["templates"]

            for template_set in template_sets:

                # retrieve template configuration
                template_data = {"name": template_set["template"]["name"]}

                template_config_list = template_set["template"]["metadataCollection"]
                for template_config in template_config_list:
                    config_array.append([template_data["name"],
                                         "",
                                         template_config.get("key"),
                                         template_config.get("value")])

                # retrieve template attribute configuration
                for attribute in template_set["attributes"]:

                    attribute_config_list = attribute["metadataCollection"]
                    for attribute_config in attribute_config_list:
                        config_array.append([
                            template_data["name"],
                            attribute["name"],
                            attribute_config.get("key"),
                            attribute_config.get("value")])

            return "\n".join([",".join(row) for row in config_array])

        except Exception as error:
            raise error

    @single_org
    def download_given_templates(self, org_id=None, template_list=None, format="csv"):
        """
        Downloads data from templates.

        :param org_id: Org where the templates exists
        :type org_id: int or str
        :param template_list: List containing the template ids
        :type template_list: list of int
        :param format: File format. Accepts "CSV" or "JSON"
        :type format: str
        :return: Text representing templates
        """
        try:

            list_templates = template_list if template_list is not None else []

            data = self.download_template(org_id=org_id, list_templates=list_templates)

            if format == "csv":
                return data

            return json.dumps(csv_to_json(csv_data=data))

        except Exception as error:
            raise error
