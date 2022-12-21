import importlib
import os

from importlib import import_module
from inspect import isabstract, isclass
from pathlib import Path
from pkgutil import iter_modules


package_dir = os.path.join(Path(__file__).resolve().parent)

for (_, module_name, _) in iter_modules([package_dir]):
    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if isclass(attribute):
            # Add the class to this package's variables, so that it became visible
            globals()[attribute_name] = attribute
