import abc
import configparser
import logging
import os

import osparc

from ._default import ServiceBase
from osparc.api import FilesApi, SolversApi
from osparc.models import File, Job, JobInputs, JobOutputs, JobStatus, Solver, Profile

# FIXME: adapt to osparc

class OsparcService(ServiceBase):

    default_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json; charset=utf-8",
    }

    host_api = "https://api.osparc.io"

    def __init__(self, config=None, connect=False) -> None:
        logging.info("Initializing Pennsieve...")
        logging.debug(str(config))

        self.set_profile(
            osparc_api_key=os.environ.get("OSPARC_API_KEY") or config.get("osparc_api_key"),
            osparc_api_secret=os.environ.get("OSPARC_API_SECRET") or config.get("osparc_api_secret")
        )

        logging.info("Profile: " + self.profile_name)
        if connect:
            self.connect()  # profile_name=self.profile_name)

    def connect(self):
        logging.info("Connecting to osparc...")

        if self.profile_name is not None:
            self._api_client.connect(profile_name=self.profile_name)
        else:
            self._api_client.connect()
        return self._api_client

    def info(self) -> str:
        return self._api_client.agent_version()

    def get_profile(self) -> str:
        users_api = osparc.UsersApi(self._api_client)
        profile = users_api.get_my_profile()
        return profile.login

    def set_profile(self, osparc_api_key, osparc_api_secret) -> str:
        cfg = osparc.Configuration(
            username=osparc_api_key,
            password=osparc_api_secret,
        )
        self._api_client = osparc.ApiClient(cfg)
        return self.get_profile()

    def close(self) -> None:
        return self._api_client.close()

    # TODO: add here an osparc-specific operation