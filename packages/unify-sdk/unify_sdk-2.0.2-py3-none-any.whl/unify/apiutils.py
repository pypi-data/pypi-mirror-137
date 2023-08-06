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
Contains helper methods
"""
import csv


def build_header(auth_token=None, org_id=None, others=None):
    """
    Creates request header

    :param auth_token: x-auth-toben to be included
    :type auth_token: str
    :param org_id: Org id where the request will be aimed
    :type org_id: int or str
    :param others: Other headers to be included.
    :type others: dict
    :return:
    """
    header = {}

    if others is not None and isinstance(others, dict):
        header.update(others)

    if auth_token is not None:
        header["x-auth-token"] = auth_token

    if org_id is not None:
        header["x-organization-id"] = str(org_id)

    return header


def tabulate_from_json(value):
    """
    Creates a table from json blob

    :param value: JSON
    :type value: dict
    :return:
    """
    tabs = {}

    for item in value:

        for header in item.keys():
            if header not in tabs:
                tabs[header] = []

            tabs[header].append(item[header])

    return tabs


def save_flow_download(name, data):
    """
    Stores the data into a temporary file

    :param name: File name
    :type name: str
    :param data: Contents
    :type data: str
    :return:
    """
    file_dir = f"{name}.csv"

    fil = open(file_dir, "wb+")

    fil.write(data)

    fil.close()

    return file_dir


def remove_special(out_file, data_array):
    """
    Removes special columns from the given file

    :param out_file: Directory where the new file is going to be written
    :type out_file: str
    :param data_array: list that contains the data to be removed
    :type data_array: list of json
    :return:
    """
    server_name_value = None

    with open(out_file, 'w+') as csv_r:

        csv_writer = csv.writer(csv_r, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        first = True

        for row_json in data_array:

            if "dataArchiveServerName" in row_json:
                server_name_value = row_json["dataArchiveServerName"]
                del row_json["dataArchiveServerName"]

            if "metricsId" in row_json:
                del row_json["metricsId"]

            if first:
                first = False
                csv_writer.writerow(row_json.keys())

            csv_writer.writerow([valu for key, valu in row_json.items()])

    return server_name_value
