import logging

from vatf.utils import config
from vatf.utils import os_proxy, config_loader
from vatf import vatf_api

import inspect
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

def _copy_config(suite_path, test_name):
    import json
    if config.get_config_path() != None:
        with os_proxy.open_to_read(config.get_config_path()) as cfg:
            with os_proxy.open_to_write(os_proxy.join(suite_path, test_name, "config.json")) as f:
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

def _create_header():
    branch = config.get_vatf_branch_to_clone()
    if branch != None and branch != "":
        branch = f"-b {branch}"
    git_clone = f'git clone {branch} https://github.com/Mamatu/vatf.git'
    _write_to_script("import os")
    _write_to_script(f"os.system('rm -rf vatf')")
    _write_to_script(f"os.system('{git_clone}')")
    _write_to_script("from vatf import vatf_api")
    _write_to_script("from vatf.utils import config")
    _write_to_script("config.set_config_path('./config.json')")
    _write_to_script("from vatf.api import audio, player, wait, shell, mkdir")
    _write_to_script("vatf_api.set_api_type(vatf_api.API_TYPE.EXECUTOR)")

def create_test(suite_path, test_name, test):
    _create_test_dir(suite_path, test_name)
    _create_run_sh_script(suite_path, test_name)
    _copy_config(suite_path, test_name)
    global _test_py_file
    _create_header()
    test()
    code_lines = inspect.getsourcelines(test)
    for line in code_lines[0][1:]:
        line = textwrap.dedent(line)
        _write_to_script(line, newLine = False)

def create_tests(suite_path, **kwargs):
    for k,v in kwargs.items():
        if isinstance(v, tuple):
            create_test(suite_path, test_name = k, test = v[0], cleanup = v[1])
        else:
            create_test(suite_path, test_name = k, test = v)
