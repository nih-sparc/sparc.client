import copy
from http import HTTPStatus
from pathlib import Path
from typing import Any, TypeAlias
from unittest.mock import MagicMock
from zipfile import ZipFile

import osparc
import pytest
from pytest import MonkeyPatch
from pytest_mock import MockerFixture

from sparc.client.services.o2sparc import O2SparcService, O2SparcSolver

EnvVarsDict: TypeAlias = dict[str, str]
Solver_Dict: TypeAlias = dict[str, str]


def generate_dummy_job(inputs: osparc.JobInputs) -> osparc.Job:
    """
    Returns a dummy job given JobInputs
    """
    return osparc.Job(
        inputs,
        name="my_job",
        inputs_checksum=10,
        created_at=10.4,
        runner_name="my_runner",
        url="my_url",
        runner_url="my_runner_url",
        outputs_url="outputs_url",
    )


def create_job_mock(self, solver_id, solver_version, inputs) -> osparc.Job:
    create_job_mock.inputs = copy.copy(inputs)
    return generate_dummy_job(osparc.JobInputs(inputs))


def upload_file_mock(self, file: Path) -> osparc.File:
    upload_file_mock.input = file
    return osparc.File(id=0, filename=file.name)


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


@pytest.fixture
def dummy_solver(mocker: MockerFixture, mock_envs: EnvVarsDict) -> O2SparcSolver:
    """
    Returns a O2SparcSolver "containing" a mock osparc.Solver
    """
    cfg: osparc.Configuration = osparc.Configuration()
    cfg.host = mock_envs["O2SPARC_HOST"]
    cfg.username = mock_envs["O2SPARC_USERNAME"]
    cfg.password = mock_envs["O2SPARC_PASSWORD"]
    api_client: osparc.ApiClient = osparc.ApiClient(cfg)

    osparc_solver: osparc.Solver = osparc.Solver(
        title="sleeper",
        id="simcore/services/comp/itis/sleeper",
        version="1.2.3",
        maintainer="me",
        url="123",
    )
    mocker.patch("osparc.SolversApi.get_solver_release", return_value=osparc_solver)
    mocker.patch("osparc.SolversApi.create_job", create_job_mock)
    mocker.patch("osparc.SolversApi.start_job", return_value=None)
    mocker.patch("osparc.FilesApi.upload_file", upload_file_mock)
    sd: Solver_Dict = {
        "solver_key": "simcore/services/comp/itis/sleeper",
        "solver_version": "1.2.3",
    }
    return O2SparcSolver(api_client, sd["solver_key"], sd["solver_version"])


@pytest.fixture
def dummy_job_status() -> tuple[dict[str, Any], osparc.JobStatus]:
    status = {
        "job_id": "123",
        "progress": 34,
        "started_at": 3.5,
        "state": "in_progress",
        "stopped_at": 10.5,
        "submitted_at": 20.4,
    }
    return (status, osparc.JobStatus(**status))


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


def test_submit_job(tmp_path: Path, mocker: MockerFixture, dummy_solver: O2SparcSolver):
    """
    Test submit_job method
    """

    # test job inputs are submitted correctly
    job_inputs: dict[str, Any] = {"my_float": 4.36, "my_int": 375, "my_str": "something"}
    dummy_solver.submit_job(job_inputs)
    for key in job_inputs:
        assert create_job_mock.inputs.values[key] == job_inputs[key]

    # test directory are not valid job inputs
    job_inputs: dict[str, Any] = {"my_dir": tmp_path}
    with pytest.raises(RuntimeError) as exc_info:
        dummy_solver.submit_job(job_inputs)

    # test files are valid input files
    tmp_file: Path = tmp_path / "test_file.txt"
    tmp_file.write_text("hello from test")
    job_inputs: dict[str, Any] = {"my_file": tmp_file}
    dummy_solver.submit_job(job_inputs)


def test_job_status(
    mocker: MockerFixture,
    dummy_solver: O2SparcSolver,
    dummy_job_status: tuple[dict[str, Any], osparc.JobStatus],
):
    """
    Tests that the solver can correctly return the job status job progress
    """
    job_inputs: dict[str, Any] = {"my_float": 4.36}
    mocker.patch("osparc.SolversApi.inspect_job", return_value=dummy_job_status[1])

    job_id = dummy_solver.submit_job(job_inputs)

    assert dummy_solver.get_job_progress(job_id) == float(dummy_job_status[0]["progress"] / 100)
    assert dummy_solver.job_done(job_id)


def test_get_job_results(
    mocker: MockerFixture,
    dummy_solver: O2SparcSolver,
    dummy_job_status: tuple[dict[str, Any], osparc.JobStatus],
):

    job_inputs: dict[str, Any] = {"my_float": 4.36}
    results: dict[str, Any] = {"my_result": 2.34}
    mocker.patch(
        "osparc.SolversApi.get_job_outputs",
        return_value=osparc.JobOutputs(job_id="123", results=results),
    )
    mocker.patch("osparc.SolversApi.inspect_job", return_value=dummy_job_status[1])

    job_id = dummy_solver.submit_job(job_inputs)
    dummy_results = dummy_solver.get_results(job_id)
    for key in results:
        assert results[key] == dummy_results[key]


def test_get_log(tmp_path: Path, mocker: MockerFixture, dummy_solver: O2SparcSolver):
    """
    Test we can unzip log files
    """
    # setup logzip
    name: str = "my_log_file"
    content: str = "this is my logfile"
    my_file = tmp_path / name
    my_file.write_text(content)
    zipf = ZipFile(tmp_path / "log.zip", "w")
    zipf.write(my_file, my_file.relative_to(tmp_path))
    zipf.close()

    # mock osparc method for getting logs
    mocker.patch("osparc.SolversApi.get_job_output_logfile", return_value=zipf.filename)

    # call solver to check we can retrieve dummy log
    log_dir = dummy_solver.get_job_log("job_id")
    assert (Path(log_dir.name) / name).is_file()
    log_content = (Path(log_dir.name) / name).read_text()
    assert content == log_content
