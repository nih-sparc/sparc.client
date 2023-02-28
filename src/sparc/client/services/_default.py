from abc import ABC, abstractmethod
from typing import Optional


class ServiceBase(ABC):
    """An abstract class determining functions of Sparc Client modules

    Attributes:
    -----------
    config : dict
        Dictionary of config variables for the module implementic ServiceBase.
    connect : bool
        Determines if module should be automatically connected.
    args : dict
        All other positional arguments.
    kwargs : dict
        All other keyword arguments.

    Methods:
    --------
    connect(*args, **kwargs) -> Optional
        Connects a given module to Sparc Client.
    info(*args, **kwargs) -> str
        Returns information on the module (e.g. its version).
    get_profile(*args, **kwargs) -> str
        Returns the currently used profile.
    set_profile(*args, **kwargs) -> str
        Sets the new profile.
    close(*args, **kwargs) -> None
        Closes connection with the module.
    """

    @abstractmethod
    def __init__(self, config, connect: bool, *args, **kwargs) -> None:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def connect(self, *args, **kwargs) -> Optional:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def info(self, *args, **kwargs) -> str:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def get_profile(self, *args, **kwargs) -> str:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def set_profile(self, *args, **kwargs) -> str:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def close(self, *args, **kwargs) -> None:
        raise NotImplementedError  # pragma: no cover
