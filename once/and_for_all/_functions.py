import functools
import inspect
import types
from importlib import import_module
from pathlib import Path
from typing import Callable


from ._base import Base


class Functions(Base):
    def apply_decorator(self, decorator: Callable[[Callable], Callable]):
        module = self._module
        if not module:
            module = self.identify_caller()

        for sub_module, name, obj in self.iterate_modules(module):
            if self.is_equal(obj, decorator):
                continue
            
            if inspect.isfunction(obj):
                new_func = decorator(obj)

                setattr(new_func, "__once_last_decorator__", decorator.__name__)
                setattr(sub_module, name, new_func)
        
        return self 