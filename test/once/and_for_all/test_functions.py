import functools
import re

import isort
import test_package

import once


def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return "Test"
    
    return wrapper
    

def decorator_double(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result * 2
    
    return wrapper


def test_once_decorates_functions_correctly():
    once.and_for_all.Functions().in_module(test_package).apply_decorator(decorator)

    to_test_1 = test_package._test_module_1.some_function("Called")
    te_test_2 = test_package._test_module_2.some_function("Called")
    assert to_test_1 == "Test"
    assert te_test_2 == "Test"


def test_once_decorates_functions_correctly_in_module():
    once.and_for_all.Functions().in_module(test_package._test_module_1).apply_decorator(decorator)

    to_test_1 = test_package._test_module_1.some_function("Called")
    te_test_2 = test_package._test_module_2.some_function("Called")
    assert to_test_1 == "Test"
    assert te_test_2 == "Function called with arg: Called"


def test_once_decorates_functions_correctly_without_module():
    once.and_for_all.Functions().apply_decorator(decorator)

    config = isort.Config()
    print(config.known_first_party)
    to_test_1 = test_package._test_module_1.some_function("Called")
    te_test_2 = test_package._test_module_2.some_function("Called")
    assert to_test_1 == "Test"
    assert te_test_2 == "Test"


def test_once_decorates_functions_correctly_with_exclude():
    once.and_for_all.Functions().in_module(test_package).exclude(["_test_module_1"], None).apply_decorator(decorator)

    to_test_1 = test_package._test_module_1.some_function("Called")
    te_test_2 = test_package._test_module_2.some_function("Called")
    assert to_test_1 == "Function called with arg: Called"
    assert te_test_2 == "Test"


def test_once_decorates_functions_correctly_with_exclude_pattern():
    (once.and_for_all
        .Functions()
        .in_module(test_package)
        .exclude(None, re.compile(r"^_test_module.*"))
        .apply_decorator(decorator)
    )

    to_test_1 = test_package._test_module_1.some_function("Called")
    te_test_2 = test_package._test_module_2.some_function("Called")
    assert to_test_1 == "Function called with arg: Called"
    assert te_test_2 == "Function called with arg: Called"


def test_once_decorates_functions_correctly_with_multiple_decorators():
    (once.and_for_all
        .Functions()
        .in_module(test_package)
        .exclude(["_test_module_2"])
        .apply_decorator(decorator)
        .apply_decorator(decorator_double)
    )

    to_test_1 = test_package._test_module_1.some_function("Called")
    te_test_2 = test_package._test_module_2.some_function("Called")
    assert to_test_1 == "TestTest"
    assert te_test_2 == "Function called with arg: Called"