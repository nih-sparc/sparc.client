from ._version import __version__ as package_version
from .client import SparcClient

__version__ = package_version
__all__: tuple[str, ...] = [
    "SparcClient",
    # "services.pennsieve.PennsieveService"
]
