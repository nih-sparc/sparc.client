import logging
import os
from configparser import SectionProxy
from typing import Any, TypeAlias

import osparc
from osparc.models.profile import Profile

from ._default import ServiceBase

ConfigDict: TypeAlias = dict[str, Any] | SectionProxy


class OsparcService(ServiceBase):
    host_api = "https://api.osparc.io"

    def __init__(self, config: ConfigDict | None = None, connect: bool = False) -> None:
        config = config or {}

        self._api_client: osparc.ApiClient

        logging.info("Initializing Osparc...")
        logging.debug("%s", f"{config}")

        self.set_profile(
            osparc_api_key=os.environ.get("OSPARC_API_KEY") or config.get("osparc_api_key"),
            osparc_api_secret=os.environ.get("OSPARC_API_SECRET")
            or config.get("osparc_api_secret"),
        )

        logging.info("Initialized osparc to %s", user_name)

    def connect(self):
        logging.info("Connecting to osparc...")
        return self._api_client

    def info(self) -> str:
        return self._api_client.agent_version()

    def get_profile(self) -> str:
        users_api = osparc.UsersApi(self._api_client)
        profile: Profile = users_api.get_my_profile()
        return profile.login

    def set_profile(self, osparc_api_key, osparc_api_secret) -> str:
        cfg = osparc.Configuration(
            username=osparc_api_key,
            password=osparc_api_secret,
        )
        self._api_client = osparc.ApiClient(cfg)
        self._users_api = osparc.UsersApi(self._api_client)

    def close(self) -> None:
        return self._api_client.close()

    # TODO: add here an osparc-specific operation
