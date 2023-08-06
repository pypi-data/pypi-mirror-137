import pkgutil
from importlib import import_module
from inspect import isclass
from pathlib import Path

from taskimporter.task_managers.base_task_manager import BaseTaskManager

task_managers = {}

package_dir = Path(__file__).resolve().parent
for (_, module_name, _) in pkgutil.iter_modules([str(package_dir)]):
    module = import_module(f"{__name__}.{module_name}")

    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        if isclass(attribute) and issubclass(attribute, BaseTaskManager) and attribute is not BaseTaskManager:
            task_managers[attribute.name] = attribute
