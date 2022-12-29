__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import logging

from vatf.utils import config_handler
from vatf.utils import os_proxy
from vatf import vatf_api

import inspect
import json
import textwrap

_test_py_file = None
_test_name = None

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

def _create_pytest_file(suite_path, test_name):
    global _test_py_file
    _test_py_file = os_proxy.join(suite_path, test_name, "test.py")
    _test_py_file = os_proxy.open_to_write(_test_py_file)

def _create_assets_dir(suite_path, test_name):
    assets_path = os_proxy.join(suite_path, test_name, "assets")
    os_proxy.mkdir(assets_path)
    os_proxy.mkdir(os_proxy.join(assets_path, "audio_files"))

def _process_configs(suite_path, test_name, config_pathes):
    if config_pathes is None:
        config_pathes = []
    if isinstance(config_pathes, str):
        config_pathes = [config_pathes]
    config_handler.init_configs(config_pathes)
    for config_path in config_pathes:
        with os_proxy.open_to_read(config_path) as cfg:
            config_basename = os_proxy.basename(config_path)
            with os_proxy.open_to_write(os_proxy.join(suite_path, test_name, config_basename)) as f:
                f.write(cfg.read())

def _create_tools(config):
    logging.info(f"{_create_tools.__name__} create tools in {config.test_path}")
    import shutil
    import pathlib
    toolsPath = os_proxy.join(config.test_path, "tools")
    os_proxy.remove(toolsPath)
    filedir = pathlib.Path(__file__).parent.resolve()
    os_proxy.copy(f'{filedir}/tools', toolsPath)

def _create_test_dir(suite_path, test_name):
    global _test_name
    _test_name = test_name
    os_proxy.mkdir(os_proxy.join(suite_path, test_name))
    _create_assets_dir(suite_path, test_name)
    _create_pytest_file(suite_path, test_name)

def _create_run_sh_script(suite_path, test_name):
    sh_run = os_proxy.join(suite_path, test_name, "run_test.sh")
    sh_run = os_proxy.open_to_write(sh_run)
    os_proxy.writeln_to_file(sh_run, "#!/bin/bash\n")
    os_proxy.write_to_file(sh_run, "PYTHONPATH=. python3 test.py")

def _copy_tools(suite_path, test_name):
    tools_path = os_proxy.join(suite_path, test_name, "tools")
    os_proxy.copy("./vatf/tools", tools_path)

def get_test_name():
    global _test_name
    return _test_name

def _write_to_script(line, newLine = True):
    global _test_py_file
    if newLine:
        os_proxy.writeln_to_file(_test_py_file, line)
    else:
        os_proxy.write_to_file(_test_py_file, line)

def verify_call(call):
    logging.debug(f"Registered {call}")

def create_call(module, function_name, *args, **kwargs):
    global _test_py_file
    if not vatf_api.is_registered(module, function_name):
        raise Exception(f"{function_name} is not registered as function of executing api")
    funcall = make_pycall(function_name, *args, **kwargs)
    verify_call(f"{module}.{funcall}")

_lines_to_replace = {}

def replace_call(module, function_name, func_to_replace, *args, **kwargs):
    global _test_py_file, _lines_to_replace
    if not vatf_api.is_registered(module, function_name):
        raise Exception(f"{function_name} is not registered as function of executing api")
    funcall = make_pycall(function_name, *args, **kwargs)
    _lines_to_replace[func_to_replace] = funcall
    verify_call(f"{module}.{funcall}")

def get_test_py_header(config_pathes = None):
    if config_pathes is None:
        config_pathes = config.get_configs_basename()
    header1 = [
        "import os",
        "os.system('rm -rf vatf')",
        "os.system('git clone {branch} https://github.com/Mamatu/vatf.git')",
        "from vatf import vatf_init, vatf_api",
        "from vatf.utils import config"
    ]
    header2 = [f"config.load('./{config}')" for config in config_pathes]
    header3 = [
        "from vatf.api import audio, player, wait, shell, mkdir, log_snapshot",
        "vatf_api.set_api_type(vatf_api.API_TYPE.EXECUTOR)"
    ]
    return header1 + header2 + header3

def _create_header(configs):
    output = config_handler.handle(["vatf.branch"], custom_format = {"session_path" : ""})
    branch = output["vatf.branch"]
    if branch is not None and branch != "":
        branch = f"-b {branch}"
    else:
        branch = ""
    for line in get_test_py_header(configs):
        _write_to_script(line.format(branch = branch))

def create_test(suite_path, test_name, test, set_up = None, tear_down = None, configs = None):
    def execute(_callable, code_lines):
        _callable()
        _code_lines = inspect.getsourcelines(_callable)
        return code_lines + _code_lines[0][1:]
    _create_test_dir(suite_path, test_name)
    _create_run_sh_script(suite_path, test_name)
    _process_configs(suite_path, test_name, configs)
    global _test_py_file
    _create_header(configs)
    code_lines = []
    if set_up: code_lines = execute(set_up, code_lines)
    code_lines = execute(test, code_lines)
    if tear_down: code_lines = execute(tear_down, code_lines)
    for line in code_lines:
        line = textwrap.dedent(line)
        _write_to_script(line, newLine = False)
    global _lines_to_replace
    _lines_to_replace = {}

def create_tests(suite_path, set_up = None, tear_down = None, configs = None, **kwargs):
    for k,v in kwargs.items():
        create_test(suite_path, test_name = k, test = v, set_up = set_up, tear_down = tear_down, configs = configs)
