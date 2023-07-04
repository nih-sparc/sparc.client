import logging
import os
from configparser import SectionProxy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, TypeAlias
from zipfile import ZipFile, is_zipfile

import osparc
from osparc.models.profile import Profile

from ._default import ServiceBase

ConfigDict: TypeAlias = dict[str, Any] | SectionProxy
UserNameStr: TypeAlias = str
JobId: TypeAlias = str


class O2SparcSolver:
    """
    Wrapper for osparc.Solver
    """

    def __init__(self, api_client: osparc.ApiClient, solver_key: str, solver_version: str):
        self._files_api: osparc.FilesApi = osparc.FilesApi(api_client)
        self._solvers_api: osparc.SolversApi = osparc.SolversApi(api_client)
        self._solver: osparc.Solver = self._solvers_api.get_solver_release(
            solver_key, solver_version
        )
        self._jobs: list[osparc.Job] = []

    def submit_job(self, job_inputs: dict[str, str | int | float | Path]) -> JobId:
        """
        Submit a job to the solver/computational service.
        The fields of the job_inputs must be one of the following types:
            str, int, float, pathlib.Path,
        where the pathlib.Path i is used to pass a file to the solver.
        """
        inputs: dict[str, str | int | float | osparc.File] = {}
        for key in job_inputs:
            inp = job_inputs[key]
            if isinstance(inp, Path):
                if not inp.is_file():
                    raise RuntimeError(f"Input {key} is not a file.")
                inputs[key] = self._files_api.upload_file(inp)
            else:
                inputs[key] = inp

        job: osparc.Job = self._solvers_api.create_job(
            self._solver.id, self._solver.version, osparc.JobInputs(inputs)
        )
        self._jobs.append(job)
        self._solvers_api.start_job(self._solver.id, self._solver.version, job.id)
        return job.id

    def get_job_progress(self, job_id: JobId) -> float:
        """
        Returns the progress of the job, i.e. a float between 0.0 and 1.0 with a 1.0 indicating that the job is done.
        """
        status: osparc.JobStatus = self._solvers_api.inspect_job(
            self._solver.id, self._solver.version, job_id
        )
        return float(status.progress / 100)

    def job_done(self, job_id: JobId) -> bool:
        """
        Returns true if the job is done. False otherwise.
        """
        status: osparc.JobStatus = self._solvers_api.inspect_job(
            self._solver.id, self._solver.version, job_id
        )
        return status.stopped_at

    def get_results(self, job_id: JobId) -> dict[str, Any]:
        """
        Returns a dictionary containing the results from a job.
        """
        if not self.job_done(job_id):
            raise RuntimeError(f"The job with job_id={job_id} is not done yet.")
        outputs: osparc.JobOutputs = self._solvers_api.get_job_outputs(
            self._solver.id, self._solver.version, job_id
        )
        results: dict[str, Any] = {}
        for key in outputs.results:
            r = outputs.results[key]
            if isinstance(r, dict) and ("filename" in dir(r)) and ("id" in dir(r)):
                download_path: str = self._files_api.download_file(file_id=r.id)
                results[key] = Path(download_path)
            else:
                results[key] = r
        return results

    def get_job_log(self, job_id: JobId) -> TemporaryDirectory:
        """
        Returns a tempfile.TemporaryDirectory containing the log files from the job
        """
        logfile_path: str = self._solvers_api.get_job_output_logfile(
            self._solver.id, self._solver.version, job_id
        )
        if not (Path(logfile_path).is_file() and is_zipfile(logfile_path)):
            raise RuntimeError("Could not download logfiles")

        tmp_dir = TemporaryDirectory()
        with ZipFile(logfile_path) as zf:
            zf.extractall(tmp_dir.name)
        os.remove(logfile_path)
        return tmp_dir


class O2SparcService(ServiceBase):
    """Wraps osparc python client library and fulfills ServiceBase interface"""

    def __init__(self, config: ConfigDict | None = None, connect: bool = True) -> None:
        config = config or {}
        logging.info("Initializing o2sparc...")
        logging.debug("%s", f"{config=}")

        kwargs = {}
        for name in ("host", "username", "password"):
            env_name = f"O2SPARC_{name.upper()}"
            config_name = env_name.lower()
            value = os.environ.get(env_name) or config.get(config_name)
            if value is not None:
                kwargs[name] = value

        logging.debug(f"Config arguments:{kwargs}")
        configuration = osparc.Configuration(**kwargs)

        # reuses profile-name from penssieve to set debug mode
        profile_name = config.get("pennsieve_profile_name", "prod")
        configuration.debug = profile_name == "test"

        self._client = osparc.ApiClient(configuration=configuration)

        if connect:
            self.connect()

    def connect(self) -> osparc.ApiClient:
        """Explicitily initializes client pool (not required)"""
        p = self._client.pool
        logging.debug("%s was initialized", p)
        return self._client

    def info(self) -> str:
        """Returns the version of osparc client."""
        return self._client.user_agent.split("/")[1]

    def get_profile(self) -> UserNameStr:
        """Returns currently user profile.

        Returns:
        --------
        A string with username.
        """
        users_api = osparc.UsersApi(self._client)
        profile: Profile = users_api.get_my_profile()
        return profile.login

    def set_profile(self, username: str, password: str) -> UserNameStr:
        """Changes to a different user profile

        Parameters:
        -----------
        username :str
            API user key
        password :str
            API user secret

        Returns:
        --------
        A string with username.
        """
        cfg = self._client.configuration
        cfg.username = username
        cfg.password = password
        return self.get_profile()

    def close(self) -> None:
        """Closes the osparc client."""
        self._client.close()

    def get_solver(self, solver_key: str, solver_version: str) -> O2SparcSolver:
        """
        Returns a computational service (solver) to which jobs can be submitted.
        """
        return O2SparcSolver(self._client, solver_key, solver_version)
