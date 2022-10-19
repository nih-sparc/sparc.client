import pytest
from sparc.client import Agent


def test_alive():
    agent=Agent()
    assert agent.alive()