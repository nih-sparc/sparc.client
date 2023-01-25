import os
from importlib import import_module
from inspect import isabstract, isclass
from pathlib import Path
from pkgutil import iter_modules

from ._default import ServiceBase

package_dir = os.path.join(Path(__file__).resolve().parent)


# The following loop iterates through the files in the current directory,
# checks for the python classes extending ServiceBase and adds them to global variables.
for _, module_name, _ in iter_modules([package_dir]):
    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if isclass(attribute) and issubclass(attribute, ServiceBase) and not isabstract(attribute):
            # Add the class to this package's variables, so that it became visible
            globals()[attribute_name] = attribute
