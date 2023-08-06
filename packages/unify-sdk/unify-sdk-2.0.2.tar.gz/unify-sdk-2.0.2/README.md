# Element Unify Python SDK

The Unify Python SDK is a library to interact with Element Unify. This SDK is intended for
developers who are building connectors and automation software that interfaces with
Element Unify.

## User Information

This section is intended for users of the Unify Python SDK. This includes
developers who are building connectors, integrations, and automation that interfaces
with Element Unify. For developers looking to contribute to the SDK, see the
[Developer Information](#developer-information) section.

## Installation
You can install the Unify Python SDK from [PyPI](pypi.org/project/unify-sdk):

`pip install unify-sdk`

### Using the Unify Python SDK with virtualenv

This assumes you have installed an appropriate version virtualenv, python, and
other associated tools. This also assumes you have an existing python project
you'd like to import into, in this case `my-project`.

    mkdir path/to/my-project; cd path/to/my-project
    virtualenv venv
    source venv/bin/activate
    echo unify-sdk >> requirements.txt

Then, in your python import section add the following line:

    from unify.apimanager import ApiManager

### Documentation
Developer guide is found in the Unify API Documentation Portal under the Unify Python SDK section.

1. Navigate to your instance of Element Unify.
2. Log in and select your organization.
3. From the top-right menu, click on the Support icon and select API Documentation.

### Asset Access
In order to use the Unify Access package, please install psycopg2-binary.

    pip install psycopg2-binary

## Developer Information

This section is intended for developers working to extend the Unify Python SDK.

### Developer Guide

1. Fork this repository.
2. Revise files with your contributions.
3. Follow styling guides. See [Python style guide](#python-style-guide).
4. Check for lint warnings. See [Lint checking](#lint-checking).
5. Create a pull request with description of your changes.

### Python style guide

Please use the following Python style guide
[Google Python Styling guide](https://google.github.io/styleguide/pyguide.html)
### Lint checking

We usy pylint to verify lint warnings, our build system requires a linter score
of >=9.0 to pass successfully.
 
To locally check you changes
```
pip install pylint
pylint dir/to/the/file.py
```

