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
Contains helper methods for files
"""
import io
import csv


def json_to_csv(data_array, io_format=False):
    """
    Converts a json array into a csv file

    :param data_array: JSON list
    :type data_array: list
    :param io_format: Flag to return IO format
    :type io_format: bool, optional
    :return:
    """
    output = io.StringIO()

    writer = csv.writer(output, quoting=csv.QUOTE_ALL, delimiter=',')

    first = True
    columns = []
    for value in data_array:
        if first:
            first = False
            writer.writerow(value.keys())
            columns = value.keys()

        new_row = []
        for col in columns:
            new_row.append(value[col])
        writer.writerow(new_row)

    if io_format:
        return output

    return output.getvalue()


def csv_to_json(csv_data):
    """
    Creates a json obtect from a csv data

    :param csv_data: Contents in CSV format
    :type csv_data: str
    :return:
    """
    csv_file = []
    reader = csv.DictReader(io.StringIO(csv_data.decode("utf-8")))
    for row in reader:
        csv_file.append(row)

    return csv_file


def stream_iterable(container, chunk):
    """
    Generates sub chunks of the given size on the given iterable

    :param container: interable object
    :type container: interable object
    :param chunk: sub chunk size to be create
    :type chunk: int
    :return:
    """
    counter = 0
    ex = False
    while not ex:

        yield container[counter:counter + chunk]
        counter += chunk

        if counter > len(container):
            ex = True


def create_schema_dataset(csv_data, name):
    """
    Creates the schema to be used on on static route create dataset

    :param csv_data: CSV data from the source to be used
    :type csv_data: str
    :param name: Dataset name being used
    :type name: str
    :return:
    """
    schema = {
        "name": name,
        "cause": [],
        "schema": {
            "properties": {},
            "columns": []
        }
    }
    reader = csv.DictReader(io.StringIO(csv_data))
    headers = next(reader)
    for header in headers:
        schema["schema"]["columns"].append(
            {
                "column": {
                    "type": "text",
                    "properties": {}
                },
                "header": header
            }
        )

    return schema
