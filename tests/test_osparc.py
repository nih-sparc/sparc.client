from pytest_mock import MockerFixture

from sparc.client.services.osparc import OsparcService


def test_connect_no_profile(mocker: MockerFixture):
    expected = None
    mocker.patch("pennsieve2.Pennsieve.connect")
    p = OsparcService(connect=False)
    pennsieve = p.connect()
    actual = pennsieve.get_user()
    assert actual == expected


def test_connect_false_with_profile(mocker: MockerFixture, mock_user, mock_pennsieve):
    expected = "profile"
    mocker.patch("pennsieve2.Pennsieve.connect")
    mocker.patch("pennsieve2.Pennsieve.get_user", mock_user.get_user)
    mock_user.set_user("profile")
    p = OsparcService(connect=False, config={"pennsieve_profile_name": "profile"})
    pennsieve = p.connect()
    actual = pennsieve.get_user()
    assert actual == expected


def test_connect_true_with_profile(mocker: MockerFixture, mock_user, mock_pennsieve):
    expected = "test version"
    mocker.patch("pennsieve2.Pennsieve.connect", mock_pennsieve.connect)
    mocker.patch("pennsieve2.Pennsieve.agent_version", mock_pennsieve.agent_version)
    mocker.patch("pennsieve2.Pennsieve.get_user", mock_user.get_user)
    mock_user.set_user("profile")
    p = OsparcService(connect=True, config={"pennsieve_profile_name": "profile"})
    pennsieve = p.connect()
    assert pennsieve is not None
    assert pennsieve.get_user() == "profile"
    assert pennsieve.agent_version() == expected


def test_get_profile(mocker: MockerFixture, mock_pennsieve, mock_user):
    expected = "user"
    mocker.patch("pennsieve2.Pennsieve.get_user", mock_user.get_user)
    mock_user.set_user("user")

    p = OsparcService(connect=False)
    actual = p.get_profile()
    assert actual == expected


def test_set_profile(mocker: MockerFixture, mock_pennsieve):
    expected = "new user"
    mocker.patch("pennsieve2.Pennsieve.switch", mock_pennsieve.switch)

    class Manifest:
        manifest = "manifest"

        def __init__(self):
            pass

    p = OsparcService(connect=False)
    p.manifest = Manifest()
    actual = p.set_profile("new user")
    assert expected == actual


def test_info(mocker: MockerFixture, mock_pennsieve):
    expected = "test version"
    mocker.patch("pennsieve2.Pennsieve.agent_version", mock_pennsieve.agent_version)
    p = OsparcService(connect=False)
    actual = p.info()
    assert expected == actual


def test_closed(mocker: MockerFixture, mock_pennsieve):
    expected = "closed"
    mocker.patch("pennsieve2.Pennsieve.stop", mock_pennsieve.close)
    p = OsparcService(connect=False)
    actual = p.close()
    assert expected == actual