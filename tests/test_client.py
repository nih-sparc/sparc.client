import os.path

import pytest

from sparc.client import SparcClient


# Test creating a default instance
def test_class(config_file):
    c = SparcClient(connect=False, config_file=config_file)
    assert len(c.module_names) > 0


# Test config file with incorrect section pointer
def test_config_no_section(test_resources_dir):
    config_file = os.path.join(test_resources_dir, "dummy_config.ini")
    with pytest.raises(KeyError):
        SparcClient(config_file, connect=False)


# Config non-existing config
def test_config_non_existing(config_file=None):
    client = SparcClient(config_file, connect=False)
    c = client.get_config()
    assert c['global']['default_profile'] == 'default'
    assert c['default']['pennsieve_profile_name'] == 'pennsieve'


# Test proper config provided
def test_get_config(test_resources_dir):
    config_file = os.path.join(test_resources_dir, "config.ini")
    client = SparcClient(config_file, connect=False)
    c = client.get_config()
    assert c['global']['default_profile'] == 'ci'
    assert c['ci']['pennsieve_profile_name'] == 'ci'


# Test module addition
def test_failed_add_module(config_file):
    client = SparcClient(connect=False, config_file=config_file)
    with pytest.raises(ModuleNotFoundError):
        client.add_module(paths="sparc.client.xyz", connect=False)


# Test using a config with the module
def test_add_module_connect(config_file):
    sc = SparcClient(config_file=config_file, connect=False)

    expected_module_config = {"module_param": "value"}
    sc.add_module("mock_service", config=expected_module_config, connect=True)

    assert "mock_service" in sc.module_names
    assert hasattr(sc, "mock_service")

    d = sc.mock_service
    from mock_service import MockService

    assert isinstance(d, MockService)
    assert d.init_connect_arg is True
    assert d.init_config_arg == expected_module_config
    assert d.connect_method_called is True


# Test adding a Pennsieve module
def test_add_pennsieve(config_file):
    sc = SparcClient(config_file=config_file, connect=False)
    assert "pennsieve" in sc.module_names
    assert hasattr(sc, "pennsieve")
    from sparc.client.services.pennsieve import PennsieveService

    assert isinstance(sc.pennsieve, PennsieveService)


# Test connection to the module
def test_module_connect(config_file, monkeypatch):
    sc = SparcClient(config_file=config_file, connect=False)
    mock_connect_results = []

    def make_mock_connect(service_name):
        return lambda: mock_connect_results.append(service_name)

    for name in sc.module_names:
        service = getattr(sc, name)
        monkeypatch.setattr(service, "connect", make_mock_connect(name))

    sc.connect()
    assert mock_connect_results == sc.module_names
