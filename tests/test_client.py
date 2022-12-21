import pytest

from sparc.client import SparcClient


def test_init():
    a = SparcClient(connect=False)
    assert a is not None


def test_alive():
    a = SparcClient(connect=False)
    assert a.alive()
