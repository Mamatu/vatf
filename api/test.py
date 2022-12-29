__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from vatf import vatf_init
from vatf.generator import gen_tests
from vatf.utils import utils

import argparse
import inspect
import sys

_suite_path = None
_config_path = []
_parser = None

def create_test(tf):
    _arg_parse()
    set_up = get_set_up()
    tear_down = get_tear_down()
    global _suite_path, _config_path
    gen_tests.create_test(_suite_path, tf.__name__, tf, configs = _config_path, set_up = set_up, tear_down = tear_down)

def create_suite():
    _arg_parse()
    test_funcs = get_test_functions()
    for tf in test_funcs:
        create_test(tf)

def _get_exec_module():
    stack = inspect.stack()
    inspect_module = inspect.getmodule(stack[0])
    this_module = inspect.getmodule(sys.modules[__name__])
    for frame in stack:
        frame_module = inspect.getmodule(frame[0])
        if this_module != frame_module and inspect_module != frame_module:
            return frame_module
    raise Exception(f"_get_exec_module not called outside of test.py")

def _arg_parse():
    global _parser, _suite_path, _config_path
    if _parser == None:
        _parser = argparse.ArgumentParser()
        _parser.add_argument('test_args', nargs='*')
        args = _parser.parse_args()
        if len(args.test_args) < 2:
            raise Exception("It must be specified at least: 1) path where are created test directories 2) path to config")
        _suite_path = args.test_args[0]
        _config_path = args.test_args[1:]

def _is_mod_function(mod, func):
    return inspect.isfunction(func) and inspect.getmodule(func) == mod

def get_functions(_filter):
    mod = _get_exec_module()
    return [func for func in mod.__dict__.values()
            if _is_mod_function(mod, func) and _filter(func.__name__)]

def get_test_functions(test_name_prefix = "Test_"):
    return get_functions(lambda name: name.startswith(test_name_prefix))

def _get_unique(name):
    funcs = get_functions(lambda _name: _name == name)
    if len(funcs) > 1:
        raise Exception(f"More than one {name} function found!")
    return funcs[0] if len(funcs) == 1 else None

def get_set_up():
    return _get_unique(name = "set_up")

def get_tear_down():
    return _get_unique(name = "tear_down")
