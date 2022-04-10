import os_proxy
import logging

from vatf.utils.config_loader import ConfigLoader
from vatf import test_api

_test_py_file = None

def _k_repr(k):
    if isinstance(k, str):
        if k.startswith("'") and k.endswith("'"):
            return k[1:-1]
    return k

def make_pycall(function_name, *args, **kwargs):
    global _test_py_file
    funcall = f"{function_name}"
    args_array = []
    for a in args:
        args_array.append(repr(a))
    for k,v in kwargs.items():
        args_array.append(f"{_k_repr(k)} = {repr(v)}")   
    py_args = ", ".join(args_array)
    funcall = f"{funcall}({py_args})"
    return funcall

def _create(filepath, config = None, testf_ctx = None):
    global _test_py_file
    _test_py_file = os_proxy.open_to_write(filepath)

def _create_test_config(config):
    import json
    if config.data != None:
        with open(f'{config.test_path}/config.json', 'w') as f:
            json.dump(config.data, f)

def _create_tools(config):
    logging.info(f"{_create_tools.__name__} create tools in {config.test_path}")
    import shutil
    import pathlib
    toolsPath = os.path.join(config.test_path, "tools")
    if os.path.exists(toolsPath):
        shutil.rmtree(toolsPath)
    filedir = pathlib.Path(__file__).parent.resolve()
    shutil.copytree(f'{filedir}/tools', toolsPath)

def _create_test_dir(config, suite_path, filepath, testf_ctx):
    global _test_py_file
    if config is None:
        config = Config("config.json")
    logging.debug(f"Config: {config.__dict__}")
    setattr(config, 'searched_audio_files_pathes', config.searched_audio_files_pathes)
    setattr(config, 'suite_path', suite_path)
    setattr(config, 'test_path', os.path.dirname(filepath))
    setattr(config, 'rel_audio_files_path_in_test', "assets/audio_files")
    setattr(config, 'abs_audio_files_path_in_test', os.path.join(config.test_path, config.rel_audio_files_path_in_test))
    os_proxy.mkdir(config.__dict__['abs_audio_files_path_in_test'])
    _create_test_config(config)
    _create(filepath, config, testf_ctx)
    _create_tools(config)

def create_call(function_name, *args, **kwargs):
    global _test_py_file
    if not test_api.is_registered(function_name):
        raise Exception(f"{function_name} is not registered as function of executing api")
    funcall = make_pycall(function_name, *args, **kwargs)
    _test_py_file.write(f"{funcall}\n")

def create_test(config, suite_path, test_name, test, cleanup = None):
    global _run_test, _cleanup_test, _test_py_file
    test_file_path = os.path.join(suite_path, test_name)
    os_proxy.mkdir(test_file_path)
    run_test_script = os.path.join(test_file_path, _run_test)
    _create_test_dir(config, suite_path, run_test_script, TestFContextWithInit)
    test()

def create_tests(config, suite_path, **kwargs):
    test_names = []
    for k,v in kwargs.items():
        if isinstance(v, tuple):
            create_test(config, suite_path, test_name = k, test = v[0], cleanup = v[1])
        else:
            create_test(config, suite_path, test_name = k, test = v)
        test_names.append (k)
    run_suite_script = os.path.join(suite_path, _run_suite)
    _create(run_suite_script)
