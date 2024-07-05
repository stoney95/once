import functools
from importlib import import_module
import inspect
from pathlib import Path
import re
import types
from abc import ABC

import isort
import pkg_resources

class Base(ABC):
    _module: types.ModuleType = None
    _exclude_names: list[str] = None
    _exclude_pattern: re.Pattern = None

    def in_module(self, module: types.ModuleType):
        self._module = module
        return self
    
    def exclude(self, names: list[str]=None, pattern: re.Pattern=None):
        self._exclude_names = names
        self._exclude_pattern = pattern
        return self
    
    def identify_caller(self):
        caller_frame = inspect.getouterframes(inspect.currentframe())[2]
        file_path = caller_frame.filename

        module_name = Path(file_path).stem
        module = import_module(module_name)
        
        return module
    
    def is_equal(self, obj1, obj2):
        if hasattr(obj1, "__name__") and hasattr(obj2, "__name__"):
            return obj1.__name__ == obj2.__name__
    
    # @functools.cache
    def iterate_modules(self, module: types.ModuleType):
        def is_builtin(_module):
            return isort.place_module(_module.__name__) == "STDLIB"
            
        def is_external(_module):
            if "site-packages" in inspect.getfile(_module):
                return True
            
            try:
                pkg_resources.get_distribution(_module.__name__)
                return True
            except pkg_resources.DistributionNotFound:
                pass
            except pkg_resources.extern.packaging.requirements.InvalidRequirement:  # type: ignore
                pass
            except ValueError:
                pass

            return False
        
        
        if is_builtin(module):
            return
        if is_external(module):
            return

        for name, obj in inspect.getmembers(module):
            if name.startswith('__'):
                continue
            if name == "once":
                continue
            if self._exclude_names and name in self._exclude_names:
                continue
            if self._exclude_pattern and self._exclude_pattern.match(name):
                continue

            if not inspect.ismodule(obj):
                yield module, name, obj
                continue

            yield from self.iterate_modules(obj)