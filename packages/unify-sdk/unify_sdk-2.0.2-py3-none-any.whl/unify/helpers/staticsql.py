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
This file contains static SQL queries that can be used in asset access
"""
ALL_TABLES = (
    "SELECT relname AS DataBase "
    "FROM pg_catalog.pg_class "
    "WHERE relnamespace={} ORDER BY relname DESC"
)

OID_QUERY = (
    "SELECT oid FROM pg_catalog.pg_namespace "
    "WHERE nspname='org_{}'"
)
