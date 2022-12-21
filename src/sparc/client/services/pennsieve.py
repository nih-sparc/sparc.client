import abc
import configparser
import logging
import os

from pennsieve2 import Pennsieve

from ._default import ServiceBase


class PennsieveService(ServiceBase):

    default_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json; charset=utf-8",
    }

    host_api = "https://api.pennsieve.io"

    def __init__(self, config=None, connect=False) -> None:
        logging.info("Initializing Pennsieve...")
        logging.debug(str(config))

        self.Pennsieve = Pennsieve(connect=False)
        if config is not None:
            self.profile_name = config.get("pennsieve_profile_name")
        else:
            self.profile_name = None

        logging.info("Profile: " + self.profile_name)
        if connect:
            self.connect()  # profile_name=self.profile_name)

    def connect(self):
        logging.info("Connecting to Pennsieve...")

        if self.profile_name is not None:
            self.Pennsieve.connect(profile_name=self.profile_name)
        else:
            self.Pennsieve.connect()
        return self.Pennsieve

    def info(self) -> str:
        return self.Pennsieve.agent_version()

    def get_profile(self) -> str:
        return self.Pennsieve.user.whoami()

    def set_profile(self, profile_name) -> str:
        return self.Pennsieve.user.switch(profile_name)

    def close(self) -> None:
        return self.Pennsieve.close()

    def list_datasets(
        self, limit=10, offset=0, ids=None, tags=None, orderBy=None, orderDirection=None
    ) -> list:
        return self.Pennsieve.get(
            self.host_api + "/discover/datasets",
            headers=self.default_headers,
            params={
                "limit": limit,
                "offset": offset,
                "ids": ids,
                "tags": tags,
                "orderBy": orderBy,
                "orderDirection": orderDirection,
            },
        )
