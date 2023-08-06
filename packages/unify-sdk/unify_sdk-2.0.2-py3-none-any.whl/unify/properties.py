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
Contains methods to manage the properties that the SDK needs.
For example, credentials, cluster metadata.
"""

import json
import uuid
from urllib.parse import urlparse
from enum import Enum
from enum import unique
import keyring
from unify.clusters import Cluster


@unique
class ClusterSetting(Enum):
    """
    Class to store cluster data in memory
    """
    MEMORY = 1
    KEY_RING = 2
    FILE = 3

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class Properties:
    """
    Class respresenting cluster properties
    """
    def __init__(self, clusterSetting=ClusterSetting.KEY_RING):
        """
        Properties constructor

        :param clusterSetting: Cluster settings to decide if use keyring, memory or file
        :type clusterSetting: `unify.properties.Properties.Enum`
        """
        self._SYSTEM = "ah"
        self._REMOTE = "d0adae9c-a1b7-11ea-906d-acde48001122_{}"
        self._AUTHTOKEN = "c8f9465c-a1b7-11ea-906d-acde48001122_{}"
        self._USERNAME = "c2c731a4-a1b7-11ea-906d-acde48001122_{}"
        self._PASSWORD = "b901bcca-a1b7-11ea-906d-acde48001122_{}"
        self._NAMES = '23556a06-a1c0-11ea-906d-acde48001122'
        self._DEFAULT = '69a9e665-bdd0-40aa-b729-735c8997d3f6'
        self._ASSETSYNC = 'cc61e5c1-ab56-43cb-b848-f342eaafc90c_{}'

        self.clusters = {}
        self.clusterSetting = clusterSetting

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_memory_cluster(self, name):
        """
        Retrieves the cluster data from memory

        :param name: Cluster name
        :type name: str
        :return: hostname
        """
        cluster = self.clusters.get(name)

        if cluster is None:
            raise Exception('Remote server must be setup first by running')

        return cluster

    def set_default(self, name):
        """
        Sets default cluster

        :param name: Cluster name to set as default
        :type name: str
        """
        try:
            clus = keyring.get_password(self._SYSTEM, self._REMOTE.format(name))

            if clus is not None:
                keyring.set_password(self._SYSTEM, self._DEFAULT, name)
            else:
                msg = (
                    "Cluster {}  cant be found and was"
                    "not possible to set it as default".format(name)
                )
                raise Exception(msg)

        except Exception as err:
            raise err

    def get_default(self):
        """
        Returns the default cluster

        :return:
        """
        return keyring.get_password(self._SYSTEM, self._DEFAULT)

    def store_cluster(self, username, password, cluster, name=None, assetsync=True):
        """
        Stores cluster data. This method does not makes a login request.

        :param username: Username to be used as part of login credentials
        :type username: str
        :param password: Password to be used as part of login credentials
        :type password: str
        :param cluster: Cluster URL
        :type cluster: str
        :param name: Cluster name, unique identifier
        :type name: str, optional
        :param assetsync: Flag specifying if AssetSync is available
        :type assetsync: bool, optional
        :return:
        """
        if name is None:
            name = str(uuid.uuid1())[0:10]

        if self.clusterSetting is ClusterSetting.MEMORY:

            self.clusters[name] = Cluster(
                userName=username,
                password=password,
                cluster=cluster,
                token=''
            )

        else:
            self.set_password(password=password, cluster=name)
            self.set_username(username=username, cluster=name)
            self.set_remote(server_uri=cluster, name=name)
            self.set_asset_sync(assetsync=assetsync, cluster=name)

    def set_asset_sync(self, assetsync, cluster):
        """
        Overrides the assetSync value to a given cluster

        :param assetsync: New AssetSync Value
        :type assetsync: bool
        :param cluster: Cluster name
        :type cluster: str
        :return:
        """
        if self.clusterSetting is ClusterSetting.KEY_RING:
            if assetsync:
                value = "1"
            else:
                value = "0"

            keyring.set_password(self._SYSTEM, self._ASSETSYNC.format(cluster), value)

    def get_asset_sync(self, cluster):
        """
        Returns the assetSync value of a given cluster

        :param cluster: Cluster name/id
        :type cluster: str
        :return:
        """
        if self.clusterSetting is ClusterSetting.KEY_RING:

            if cluster is None:
                cluster = self.get_default()

            value = keyring.get_password(self._SYSTEM, self._ASSETSYNC.format(cluster))
            if value is None:
                raise Exception(
                    "Remote server must be setup first by running, ah cluster add")

            return bool(value == "1")

        return True

    def set_remote(self, server_uri, name=None):
        """
        Overrides cluster URL

        :param server_uri: New cluster URL
        :type server_uri: str
        :param name: Cluster name/id
        :type name: str
        :return:
        """

        try:
            result = urlparse(server_uri)
            if result.scheme == "" or result.netloc == "":
                raise Exception("Invalid url used as Remote, please use a valid URL")

            if server_uri[-1] != "/":
                server_uri = "{}/".format(server_uri)

            if self.clusterSetting is ClusterSetting.KEY_RING:

                keyring.set_password(self._SYSTEM, self._REMOTE.format(name), server_uri)

                existing = keyring.get_password(self._SYSTEM, self._NAMES)

                if existing is None:
                    existing = [name]
                else:
                    existing = json.loads(existing)
                    if name not in existing:
                        existing.append(name)

                keyring.set_password(self._SYSTEM, self._NAMES, json.dumps(existing))

            else:
                open(self._REMOTE, "w+").write(server_uri)

        except Exception as error:
            raise error

    def remove_cluster(self, name):
        """
        Removes the given cluster

        :param name: Cluster name or ID
        :type name: str
        :return:
        """
        if self.clusterSetting is ClusterSetting.KEY_RING:

            keyring.delete_password(self._SYSTEM, self._USERNAME.format(name))
            keyring.delete_password(self._SYSTEM, self._PASSWORD.format(name))
            keyring.delete_password(self._SYSTEM, self._REMOTE.format(name))
            keyring.delete_password(self._SYSTEM, self._AUTHTOKEN.format(name))

            existing = keyring.get_password(self._SYSTEM, self._NAMES)

            if existing is not None:
                existing = json.loads(existing)
                existing.remove(name)
                keyring.set_password(self._SYSTEM, self._NAMES, json.dumps(existing))

            if name == self.get_default():
                keyring.delete_password(self._SYSTEM, self._DEFAULT)

    def set_username(self, username, cluster):
        """
        Overrides the username value for a given cluster

        :param username: New username Value
        :type username: str
        :param cluster: Cluster name to be retrieved
        :type cluster: str
        :return:
        """
        if self.clusterSetting is ClusterSetting.KEY_RING:
            keyring.set_password(self._SYSTEM, self._USERNAME.format(cluster), username)

    def get_username(self, cluster):
        """
        Retrieves the username of the given cluster

        :param cluster: Cluster name to be retrieved
        :type cluster: str
        :return:
        """
        if self.clusterSetting is ClusterSetting.MEMORY:

            return self.get_memory_cluster(cluster).userName

        if self.clusterSetting is ClusterSetting.KEY_RING:

            if cluster is None:
                cluster = self.get_default()

            value = keyring.get_password(self._SYSTEM, self._USERNAME.format(cluster))
            if value is None:
                raise Exception(
                    "Remote server must be setup first by running, ah cluster add")
            return value

        return None

    def get_password(self, cluster):
        """
        Retrieves the password of the given cluster

        :param cluster: Cluster name to be retrieved
        :type cluster: str
        :return:
        """
        if self.clusterSetting is ClusterSetting.MEMORY:

            return self.get_memory_cluster(cluster).password

        if self.clusterSetting is ClusterSetting.KEY_RING:

            if cluster is None:
                cluster = self.get_default()

            value = keyring.get_password(self._SYSTEM, self._PASSWORD.format(cluster))
            if value is None:
                raise Exception(
                    "Remote server must be setup first by running, ah cluster add")
            return value

        return None

    def set_password(self, password, cluster):
        """
        Overrides the password value for a given cluster

        :param password: New password Value
        :type password: str
        :param cluster: Cluster name to be retrieved
        :type cluster: str
        :return:
        """
        if self.clusterSetting is ClusterSetting.KEY_RING:

            keyring.set_password(self._SYSTEM, self._PASSWORD.format(cluster), password)

        else:
            pass

    def get_all_clusters(self):
        """
        Retrieves the list of all stored clusters

        :return:
        """
        if self.clusterSetting is ClusterSetting.MEMORY:

            return self.clusters.values()

        if self.clusterSetting is ClusterSetting.KEY_RING:

            names = keyring.get_password(self._SYSTEM, self._NAMES)
            if names is not None:
                existing = json.loads(names)
                clusters = []
                for item in existing:
                    clusters.append(
                        {
                            "name": item,
                            "url": keyring.get_password(self._SYSTEM, self._REMOTE.format(item)),
                            "username": keyring.get_password(
                                self._SYSTEM,
                                self._USERNAME.format(item)
                            ),
                            "default": item == self.get_default(),
                            "assetsync": keyring.get_password(
                                self._SYSTEM,
                                self._ASSETSYNC.format(item)
                            ) == "1"
                        }
                    )
                return clusters

            return []

        return []

    def set_auth_token(self, token, cluster):
        """
        Stores a new authentication token

        :param token: Auth token
        :type token: str
        :param cluster: Cluster name
        :type cluster: str
        :return:
        """

        if self.clusterSetting is ClusterSetting.MEMORY:

            self.clusters[cluster].token = token

        elif self.clusterSetting is ClusterSetting.KEY_RING:

            keyring.set_password(self._SYSTEM, self._AUTHTOKEN.format(cluster), token)
        else:

            open(self._AUTHTOKEN, "w+").write(token)

    def get_auth_token(self, cluster):
        """
        Retrieves the stored authentication token. This method does not make
        a login request.

        :param cluster: Cluster name
        :type cluster: str
        :return:
        """
        if self.clusterSetting is ClusterSetting.MEMORY:

            return self.get_memory_cluster(cluster).token

        if self.clusterSetting is ClusterSetting.KEY_RING:

            if cluster is None:
                cluster = self.get_default()

            value = keyring.get_password(self._SYSTEM, self._AUTHTOKEN.format(cluster))

            return value

        try:
            return open(self._AUTHTOKEN, "r+").read()
        except Exception as err:
            raise err

    def get_remote(self, cluster):
        """
        Retrives the cluster URL

        :param cluster: Cluster name
        :type cluster: str
        :return:
        """

        if self.clusterSetting is ClusterSetting.MEMORY:

            return self.get_memory_cluster(cluster).cluster

        if self.clusterSetting is ClusterSetting.KEY_RING:

            if cluster is None:
                cluster = self.get_default()

            value = keyring.get_password(self._SYSTEM, self._REMOTE.format(cluster))
            if value is None:
                raise Exception(
                    "Remote server must be setup first by running, ah cluster add")

            return value

        try:
            return open(self._REMOTE, "r+").read()
        except Exception as err:
            raise err
