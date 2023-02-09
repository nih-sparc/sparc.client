import pytest
import os


@pytest.fixture(scope='session')
def test_dir():
    return os.path.dirname(__file__)


@pytest.fixture(scope='session')
def test_resources_dir(test_dir):
    return os.path.join(test_dir, 'resources')


@pytest.fixture(scope='session')
def config_file(test_resources_dir):
    return os.path.join(test_resources_dir, 'config.ini')
