from typing import Optional
from sparc.client.services._default import ServiceBase


class DummyService(ServiceBase):
    """A dummy class to check module import """

    def __init__(self, config=None, connect=False, *args, **kwargs) -> None:
        pass

    def connect(self, *args, **kwargs) -> Optional:
        return True

    def info(self, *args, **kwargs) -> str:
        return "info"

    def get_profile(self):
        return "get_profile"

    def set_profile(self):
        return "set_profile"

    def close(self, *args, **kwargs) -> None:
        pass
