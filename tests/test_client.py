import os.path
from pathlib import Path

import pytest

from sparc.client import SparcClient


def test_class(config_file):
    c = SparcClient(connect=False, config_file=config_file)
    assert len(c.module_names) == 1


# Config file tests
def test_config_non_existing(config_file=None):
    with pytest.raises(RuntimeError):
        a = SparcClient(config_file, connect=False)


# Test config file with incorrect section pointer
def test_config_no_section(test_resources_dir):
    config_file = os.path.join(test_resources_dir, 'dummy_config.ini')
    with pytest.raises(KeyError):
        a = SparcClient(config_file, connect=False)


def test_failed_add_module(config_file):
    client = SparcClient(connect=False, config_file=config_file)
    with pytest.raises(ModuleNotFoundError):
        client.add_module(paths='sparc.client.xyz', connect=False)


def test_add_module_connect(config_file):
    from tests.services.dummymodule import DummyService
    d = DummyService()
    print(d.get_profile())
    sc = SparcClient(config_file=config_file, connect=False)
    sc.add_module('tests.services.dummymodule', connect=True)

