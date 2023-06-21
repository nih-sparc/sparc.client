import logging
import os
from configparser import SectionProxy
from typing import Any, TypeAlias

import osparc
from osparc.models.profile import Profile

from ._default import ServiceBase

ConfigDict: TypeAlias = dict[str, Any] | SectionProxy
UserNameStr: TypeAlias = str


class OsparcService(ServiceBase):
    """Wraps osparc python client library and fulfills ServiceBase interface"""

    def __init__(self, config: ConfigDict | None = None, connect: bool = True) -> None:
        config = config or {}
        logging.info("Initializing Osparc...")
        logging.debug("%s", f"{config=}")

        # reuse
        profile_name = config.get("pennsieve_profile_name", "prod")
        if profile_name not in ["prod", "test", "ci"]:
            raise ValueError(f"Invalid {profile_name=}.")

        kwargs = {}
        for name in ("host", "username", "password"):
            env_name = f"OSPARC_{name.upper()}"
            config_name = env_name.lower()
            value = os.environ.get(env_name) or config.get(config_name)
            if value is not None:
                kwargs[name] = value

        configuration = osparc.Configuration(**kwargs)
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

    def set_profile(self, osparc_api_key: str, osparc_api_secret: str) -> UserNameStr:
        """Changes to a different user profile

        Parameters:
        -----------
        osparc_api_key : str
            API key
        osparc_api_secret : str
            API secret

        Returns:
        --------
        A string with username.
        """
        cfg = self._client.configuration
        cfg.username = osparc_api_key
        cfg.password = osparc_api_secret
        return self.get_profile()

    def close(self) -> None:
        """Closes the osparc client."""
        self._client.close()
