import pytest
import sparc.client
from sparc.client import SparcClient


def test_alive():
    a = SparcClient(connect=False)
    assert a is not None
