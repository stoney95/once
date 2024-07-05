import functools
import once

class ToTest:
    baz = 5

    def some_method(self):
        return 5

def test_once_applies_metaclass_correctly():
    class Meta(type):
        def __new__(cls, name, bases, dct):
            dct["foo"] = "bar"
            return super().__new__(cls, name, bases, dct)
        
    once.and_for_all.Classes().apply_metaclass(Meta)

    to_test = ToTest()
    assert to_test.foo == "bar"
    assert to_test.baz == 5


def test_once_decorates_class_correctly():
    def decorator(cls):
        cls.foo = "bar"
        return cls

    once.and_for_all.Classes().apply_decorator(decorator)

    to_test = ToTest()
    assert to_test.foo == "bar"
    assert to_test.baz == 5


def test_once_decorates_methods_correctly():
    def decorator(method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            return "Test"
        return wrapper

    once.and_for_all.Classes().and_only_their_methods().apply_decorator(decorator)

    to_test = ToTest()
    assert to_test.some_method() == "Test"
    assert to_test.baz == 5