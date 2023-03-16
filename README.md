# sparc.client

NIH SPARC Python Client
=======================
[![PyPI Latest Release](https://img.shields.io/pypi/v/sparc.client.svg)](https://pypi.org/project/sparc.client/)
[![pypi](https://img.shields.io/pypi/pyversions/sparc.client.svg)](https://pypi.org/project/sparc.client/)
[![Package Status](https://img.shields.io/pypi/status/sparc.client.svg)](https://pypi.org/project/sparc.client/)
[![License](https://img.shields.io/pypi/l/sparc.client.svg)](https://github.com/nih-sparc/sparc.client/blob/main/LICENSE)
[![Coverage](https://codecov.io/github/nih-sparc/sparc.client/coverage.svg?branch=main)](https://codecov.io/gh/nih-sparc/sparc.client)

# Architecture details

The sparc.client Python Client stores its configuration in the config.ini file.

The modules of sparc.client are to be defined in services/ directory and need to be derived from BaseService class (services/_default.py)
This means that they need to implement the specific functions defined in the interface, such as __init__, connect(), info(), get_profile(), set_profile() and close().
Apart from that functions, each module in the services may define their own methods (e.g. refer to services/pennsieve.py list_datasets()).


## config.ini

The configuration file has the following format:

```txt
[global]
default_profile=ci

[prod]
pennsieve_profile_name=prod

[dev]
pennsieve_profile_name=test

[ci]
pennsieve_profile_name=ci
```

[global] section defines the default profile that is to be used. This basically refers to any section in brackets that stores configuration variables. In this case it refers to 'ci' section.

Within each section, different configuration variables could be defined. In our case, the only variable that needs to be defined is pennsieve_profile_name, which is passed to the Pennsieve2 library.



# Module automatic import

Each python file in services/ folder with defined class name that is derived from BaseService is imported as a module to SparcClient class.
For example, pennsieve.py file 

```python
from sparc.client import SparcClient
a = SparcClient(connect=False, config_file='config.ini')
module = a.pennsieve.connect()
module.info() #execute internal functions of the module

# alternatively connect all the services available
a.connect()  #connect to all services

```

## Test generation - PyTest

Some good resource for implementing tests could be found at [Medium](https://medium.com/analytics-vidhya/pytest-mocking-cheatsheet-dcebd84876e3).

## Documentation - Sphinx tutorial

A fresh start for creating documentation with Sphinx could be found at [towardsdatascience](https://towardsdatascience.com/documenting-python-code-with-sphinx-554e1d6c4f6d).
To reproduce steps:

1. Create a docs folder
2. Run `sphinx-quickstart` in docs folder, fill the required prompts.
3. Edit `conf.py` and `index.rst` files to adjust them to your needs
4. Run in docs folder sphinx-apidoc -o . ../src
5. Disregard `modules.rst` and `sphinx.rst`, attach `sphinx.client` to toctree in `index.rst`
6. Run `make html` in docs folder.

# Contribution Guide

1. Define configuration variables in config.ini file (e.g  api_key, api_secret etc.)
2. Create a file in services/
3. Create a class within this file that extends BaseService
4. The class needs to define all the functions required + may add its own.

# Developer Setup

Run `pip install -e '.[test]'` to install the dependencies needed for a development environment.

Run `pytest --cov=./src` to run the tests and get a test coverage summary.

Run `pytest --cov-report html --cov=./src` to run the tests and get a full HTML coverage report output to `htmlcov`.
