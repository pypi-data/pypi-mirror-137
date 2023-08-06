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
Contains cluster definition
"""

class Cluster:
    """
    Class to store cluster data on memory
    """

    def __init__(self, userName, password, cluster, token):
        """
        Constructor

        :param userName: Cluster login username
        :type userName: str
        :param password: Cluster login password
        :type password: str
        :param cluster: Cluster url, format http://host
        :type cluster: str
        :param token: Auth token
        :type token: str
        """
        self.userName = userName
        self.password = password
        self.cluster = cluster
        self.token = token

    def get_password(self):
        """
        Get cluster password

        :return:
        """
        return self.password

    def get_username(self):
        """
        Get cluster password

        :return:
        """
        return self.userName
