import inspect
from typing import Callable, Type
from ._base import Base

class Classes(Base):
    _only_methods: bool = False

    def and_only_their_methods(self):
        self._only_methods = True
        return self

    def apply_decorator(self, decorator: Callable[[Callable], Callable]):
        module = self._module
        if not module:
            module = self.identify_caller()

        for sub_module, name, obj in self.iterate_modules(module):
            if self.is_equal(obj, decorator):
                continue

            if not inspect.isclass(obj):
                continue
            
            if self._only_methods:
                filter_members = lambda obj: inspect.isfunction(obj) and not obj.__name__.startswith("__")
                for method_name, method in inspect.getmembers(obj, filter_members):
                    setattr(obj, method_name, decorator(method))
                continue
                
            setattr(sub_module, name, decorator(obj))

        return self         


    def apply_metaclass(self, metaclass: Type):
        if self._only_methods:
            raise ValueError("Cannot apply metaclass to methods")

        module = self._module
        if not module:
            module = self.identify_caller()

        for sub_module, name, obj in self.iterate_modules(module):
            if self.is_equal(obj, metaclass):
                continue

            if inspect.isclass(obj):
                new_class = metaclass(name, (obj,), {})
                setattr(sub_module, name, new_class)
        return self 