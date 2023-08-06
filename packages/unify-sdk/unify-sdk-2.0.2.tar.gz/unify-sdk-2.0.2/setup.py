"""
Copyright 2021 Element Analytics, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import pathlib
import re
from setuptools import setup
from setuptools import find_packages
import subprocess

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text().strip()

version = os.popen('git describe --dirty').read()

setup(
    name='unify-sdk',
    version=str(version),
    description="Unify Python SDK",
    long_description=README,
    long_description_content_type='text/markdown',
    python_requires='>=3',
    packages=find_packages(),
    include_package_data=True,
    hiddenimports=[
        'keyring',
        'setuptools',
        'tabulate',
        'requests',
        'json-lines'
    ],
    install_requires=[
        'keyring',
        'setuptools',
        'tabulate',
        'requests',
        'json-lines'
    ],
    url='https://github.com/ElementAnalytics/unify-python-sdk',
    author='Element Analytics',
    author_email='platform@ean.io',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
