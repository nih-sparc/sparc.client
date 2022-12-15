import os
from abc import ABC, abstractmethod


class ServiceBase(ABC):
    @abstractmethod
    def __init__(self, connect, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def connect(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def info(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_profile(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def set_profile(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def close(self, *args, **kwargs):
        raise NotImplementedError
