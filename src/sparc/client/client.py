import logging
import os
from configparser import ConfigParser, SectionProxy
from importlib import import_module
from inspect import isabstract, isclass
from pathlib import Path
from pkgutil import iter_modules

from .services import ServiceBase


class SparcClient:
    """
    The main class of the sparc.client library.

    This class is used to connect existing modules located in <projectbase>/services folder


    Parameters:
    -----------
    config_file : str
        The location of the file in INI format that is used to extract configuration variables.
        The config file needs to define a [global] section with the name of the default profile
        (in square brackets as well) which holds environmental variables used by the modules.
        Refer to configparser for further details.
    connect : bool (True)
        Calls connect() method of each of the modules.
        By default during initialization all modules are initialized and ready to be used,
        unless connect is set to False.


    Attributes:
    -----------
    module_names : list
        Stores the list of modules that are automatically loaded from the <projectbase>/services directory.

    Methods:
    --------
    add_module(path, config, connect):
        Adds and optionally connects to a module in a given path with configuration variables defined in config.
    connect()
        Connects all the modules by calling their connect() functions.
    """

    def __init__(self, config_file: str = "config/config.ini", connect: bool = True) -> None:
        # Read config file
        if not config_file:
            raise RuntimeError("Configuration file not given")

        config = ConfigParser()

        if os.path.isfile(config_file):
            config.read(config_file)
            logging.debug(str(config))
        current_config = config["global"]["default_profile"]

        logging.debug("Using the following config:")
        logging.debug(str(config[current_config]))
        self.module_names = []

        # iterate through the modules in the current package
        package_dir = os.path.join(Path(__file__).resolve().parent, "services")

        for _, module_name, _ in iter_modules([package_dir]):
            # import the module and iterate through its attributes
            self.add_module(
                f"{__package__}.services.{module_name}", config[current_config], connect
            )

    def add_module(
        self,
        paths: str | list[str],
        config: dict | SectionProxy | None = None,
        connect: bool = True,
    ) -> None:
        """Adds and optionally connects to a module in a given path with configuration variables defined in config.

        Parameters:
        -----------
        paths : str or list[str]
            a path to the module
        config : dict or configparser.SectionProxy
            a dictionary (or Section of the config file parsed by ConfigParser) with the configuration variables
        connect : bool
            determines if the module should auto-connect
        """
        if not isinstance(paths, list):
            paths = [paths]

        for path in paths:
            module_name = path.split(".")[-1] if "." in path else path
            try:
                module = import_module(path)
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if (
                        isclass(attribute)
                        and issubclass(attribute, ServiceBase)
                        and not isabstract(attribute)
                    ):
                        # Add the class to this package's variables
                        self.module_names.append(module_name)
                        c = attribute(connect=connect, config=config)
                        setattr(self, module_name, c)
                        if connect:
                            c.connect()

            except ModuleNotFoundError:
                logging.debug(
                    "Skipping module. Failed to import from %s", f"{path=}", exc_info=True
                )
                raise

    def connect(self) -> bool:
        """Connects each of the modules loaded into self.module_names"""
        for module_name in self.module_names:
            module = getattr(self, module_name)
            if hasattr(module, "connect"):
                getattr(self, module_name).connect()
        return True
