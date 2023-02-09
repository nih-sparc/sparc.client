import pytest
import pathlib
import sys
from abc import ABCMeta

from sparc.client import SparcClient
from typing import Optional
from configparser import Error as ConfigParserError

def test_class():
    SparcClient(connect=False)



# Config file tests
def test_config_non_existing(config_file=None):
    with pytest.raises(RuntimeError):
        a = SparcClient(config_file, connect=False)


# Test config file with incorrect section pointer
def test_config_no_section(config_file='dummy_config.ini'):
    with pytest.raises(KeyError):
        a = SparcClient(config_file, connect=False)

def test_failed_add_module():
    client = SparcClient(connect=False)
    with pytest.raises(ModuleNotFoundError):
        client.add_module(paths='sparc.client.xyz', connect=False)


# ServiceBase abstract class tests
def test_abstract_init():
    from sparc.client.services._default import ServiceBase
    ServiceBase.__abstractmethods__ = set()

    class Dummy(ServiceBase):
        x: int

    assert isinstance(Dummy, ABCMeta)
    with pytest.raises(NotImplementedError):
        d=Dummy(config='config/config.ini', connect=False)


def test_abstract_methods():
    from sparc.client.services._default import ServiceBase
    ServiceBase.__abstractmethods__ = set()

    class Dummy(ServiceBase):
        x: int
        def __init__(config=None, connect=False):
            pass
    d=Dummy()

    with pytest.raises(NotImplementedError):
        d.connect()
    with pytest.raises(NotImplementedError):
        d.info()
    with pytest.raises(NotImplementedError):
        d.get_profile()
    with pytest.raises(NotImplementedError):
        d.set_profile()
    with pytest.raises(NotImplementedError):
        d.close()

