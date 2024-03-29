__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from enum import Enum

import functools
import importlib
import sys
import types

class API_TYPE(Enum):
    EXECUTOR = 1,
    GENERATOR = 2

_apiType = API_TYPE.EXECUTOR
_package = {API_TYPE.GENERATOR : "vatf.generator", API_TYPE.EXECUTOR : "vatf.executor"}
_dynamic_modules = {}

def get_package(apiType):
    global _package
    return _package[apiType]

def _get_module(import_path):
    global _dynamic_modules
    module = sys.modules.get(import_path)
    if not module:
        module = _dynamic_modules.get(import_path)
    if not module:
        raise Exception(f"Module {import_path} was not registered")
    return module

def set_api_type(apiType):
    global _apiType
    _apiType = apiType

def get_api_type():
    global _apiType
    return _apiType

def get_api(module, custom_package = None):
    global _package
    import_path = None
    if custom_package == None:
        import_path = f"{_package[get_api_type()]}.{module}"
    else:
        import_path = f"{custom_package}.{module}"
    return _get_module(import_path)

_generator_registered_api = {}

def _create_generator_module(module_name, import_path):
    global _dynamic_modules
    module = types.ModuleType(module_name)
    _dynamic_modules[import_path] = (module)
    print(f"Runtime: created module {module_name}, full import path is {import_path}")

def _create_default_generator_wrapper(module_name, f):
    """Based on http://stackoverflow.com/a/6528148/190597 (Glenn Maynard)"""
    from vatf.generator import gen_tests
    g = types.FunctionType(f.__code__, f.__globals__, name=f.__name__,
                           argdefs=f.__defaults__,
                           closure=f.__closure__)
    def wrapper(*args, **kwargs):
        gen_tests.create_call(module_name, f.__name__, *args, **kwargs)
    g = functools.update_wrapper(wrapper, f)
    g.__kwdefaults__ = f.__kwdefaults__
    print(f"Runtime: added default generator function {f.__name__} into module {module_name}")
    return g

def _add_func_to_generator_module_if_not_exists(module_name, func, import_path):
    module = _get_module(import_path)
    if not getattr(module, func.__name__, None):
        func = _create_default_generator_wrapper(module_name, func)
        setattr(module, func.__name__, func)
    else:
        print(f"Static: found static defined {func} in {module_name}")

def _create_generator_module_if_not_exists(module_name, func, import_path):
    try:
        if not _get_module(import_path):
            _create_generator_module(module_name, import_path)
    except:
        _create_generator_module(module_name, import_path)
    finally:
        _add_func_to_generator_module_if_not_exists(module_name, func, import_path)

def public_api(module_name):
    def inner(func):
        global _generator_registered_api
        if not module_name in _generator_registered_api:
            _generator_registered_api[module_name] = {}
        _generator_registered_api[module_name][func.__name__] = func
        import_path = get_package(API_TYPE.GENERATOR)
        import_path = f"{import_path}.{module_name}"
        _create_generator_module_if_not_exists(module_name, func, import_path)
        return func
    return inner

def is_registered(module, func):
    global _generator_registered_api
    if module in _generator_registered_api:
        module = _generator_registered_api[module]
        return func in module
    return False
