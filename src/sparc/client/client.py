import importlib
import logging
import os

from configparser import ConfigParser
from inspect import isclass, isabstract
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module
from .services import *


class SparcClient(object):

    module_names = []

    def __init__(self, config_file="config/config.ini", connect=True) -> None:

        # Read config file
        if not config_file:
            raise RuntimeError("Configuration file not given")

        config = ConfigParser()

        if os.path.isfile(config_file):
            config.read(config_file)
            logging.debug(str(config))
        current_config = config["global"]["default_profile"]

        logging.debug(str(current_config))

        # iterate through the modules in the current package
        package_dir = os.path.join(Path(__file__).resolve().parent, "services")

        for (_, module_name, _) in iter_modules([package_dir]):

            # import the module and iterate through its attributes
            module = import_module(f"{__package__}.services.{module_name}")
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if (
                    isclass(attribute)
                    and issubclass(attribute, ServiceBase)
                    and not isabstract(attribute)
                ):
                    # Add the class to this package's variables
                    self.module_names.append(module_name)
                    c = attribute(connect=False, config=config[current_config])
                    setattr(self, module_name, c)
                    if connect:
                        c.connect()

    def connect(self):
        for module_name in self.module_names:
            getattr(self, module_name).connect()

    def alive(self):
        return True