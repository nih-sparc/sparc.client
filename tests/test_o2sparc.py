from http import HTTPStatus
from typing import TypeAlias
from unittest.mock import MagicMock

import osparc
import pytest
from pytest import MonkeyPatch
from pytest_mock import MockerFixture

from sparc.client.services.o2sparc import O2SparcService

EnvVarsDict: TypeAlias = dict[str, str]


@pytest.fixture
def mock_envs(monkeypatch: MonkeyPatch) -> EnvVarsDict:
    envs = {
        "O2SPARC_HOST": "https://fake-api.osparc.test",
        "O2SPARC_USERNAME": "key",
        "O2SPARC_PASSWORD": "secret",
    }
    for name, value in envs.items():
        monkeypatch.setenv(name, f"{value}")
    return envs


@pytest.fixture
def mock_osparc(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "osparc.UsersApi.get_my_profile",
        return_value=osparc.Profile(
            **{
                "first_name": "James",
                "last_name": "Maxwell",
                "login": "james-maxwell@itis.swiss",
                "role": "USER",
                "groups": {
                    "me": {"gid": "123", "label": "maxy", "description": "primary group"},
                    "organizations": [],
                    "all": {"gid": "1", "label": "Everyone", "description": "all users"},
                },
                "gravatar_id": "9a8930a5b20d7048e37740bac5c1ca4f",
            }
        ),
    )


@pytest.mark.parametrize("connect", [True, False])
def test_init(mock_envs: EnvVarsDict, connect: bool):
    o2p = O2SparcService(connect=connect)

    o2p_client = o2p.connect()
    assert isinstance(o2p_client, osparc.ApiClient)

    assert o2p_client.configuration.host == mock_envs["O2SPARC_HOST"]
    assert o2p_client.configuration.username == mock_envs["O2SPARC_USERNAME"]
    assert o2p_client.configuration.password == mock_envs["O2SPARC_PASSWORD"]


def test_init_from_config_and_envs(monkeypatch: MonkeyPatch, mock_envs: EnvVarsDict):
    monkeypatch.delenv("O2SPARC_USERNAME", raising=False)
    config = {
        "o2sparc_host": "https://api.override.com",
        "o2sparc_username": "right",
        "username": "wrong",
    }

    o2p = O2SparcService(connect=False, config=config)

    o2p_client = o2p.connect()
    assert isinstance(o2p_client, osparc.ApiClient)

    assert o2p_client.configuration.host == mock_envs["O2SPARC_HOST"]
    assert o2p_client.configuration.username == config["o2sparc_username"]
    assert o2p_client.configuration.password == mock_envs["O2SPARC_PASSWORD"]


def test_connect_no_profile(mocker: MockerFixture):
    mocker.patch(
        "osparc.UsersApi.get_my_profile", side_effect=osparc.ApiException(HTTPStatus.UNAUTHORIZED)
    )

    o2p = O2SparcService(connect=False)
    assert isinstance(o2p.connect(), osparc.ApiClient)

    with pytest.raises(osparc.ApiException) as exc_info:
        _user_name = o2p.get_profile()

    error = exc_info.value
    assert error.status == HTTPStatus.UNAUTHORIZED


def test_connect_profile(mock_osparc: MagicMock):
    o2p = O2SparcService(connect=False)
    assert isinstance(o2p.connect(), osparc.ApiClient)

    assert o2p.get_profile() == "james-maxwell@itis.swiss"
    assert mock_osparc.called


def test_set_profile(mock_osparc: MagicMock):
    o2p = O2SparcService(connect=False)
    assert (
        o2p.set_profile(username="other_user_key", password="other_user_secret")
        == "james-maxwell@itis.swiss"
    )
    assert mock_osparc.called


def test_info(mocker: MockerFixture):
    o2p = O2SparcService(connect=False)
    actual = o2p.info()
    assert "0.5.0" == actual


def test_closed(mocker: MockerFixture):
    o2p = O2SparcService(connect=False)
    o2p.close()
