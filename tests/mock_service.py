from typing import Optional

from sparc.client.services._default import ServiceBase


class MockService(ServiceBase):
    """A mock class to check module import"""

    def __init__(self, config=None, connect=False, *args, **kwargs) -> None:
        self.init_config_arg = config
        self.init_connect_arg = connect
        self.connect_method_called = False

    def connect(self, *args, **kwargs) -> Optional:
        self.connect_method_called = True
        return True

    def info(self, *args, **kwargs) -> str:
        return "info"

    def get_profile(self):
        return "get_profile"

    def set_profile(self):
        return "set_profile"

    def close(self, *args, **kwargs) -> None:
        pass
