import pkgutil
import importlib

package = __name__

for _, module_name, _ in pkgutil.iter_modules(__path__):
    # print(_, module_name, _)
    importlib.import_module(f"{package}.{module_name}")