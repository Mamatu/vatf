import copy
import inspect
import logging
import sys

from vatf.utils import config_loader, os_proxy

_loaded_config = None
_config_pathes = []

def load(path):
    global _loaded_config
    loaded_config = config_loader.load(path)
    if not _loaded_config:
        _loaded_config = loaded_config
    else:
        _loaded_config = _loaded_config + loaded_config
    _config_pathes.append(path)

def reset():
    global _loaded_config, _config_pathes
    _loaded_config = None
    _config_pathes = []

def get_config_pathes():
    global _config_pathes
    return _config_pathes.copy()

def get_configs_basename():
    global _config_pathes
    return [os_proxy.basename(config) for config in _config_pathes]

def get_config():
    global _loaded_config
    return copy.deepcopy(_loaded_config)

def _handle_format(func):
    def wrapper():
        line = func()
        global _loaded_config
        for k,v in inspect.getmembers(_loaded_config):
            if line:
                line = line.format(k = v)
        return line
    return wrapper

def _handle_none(func):
    def wrapper():
        try:
            return func()
        except AttributeError:
            return None
    return wrapper

@_handle_format
@_handle_none
def get_pathes_to_audio_files_in_system():
    global _loaded_config
    if _loaded_config:
        return _loaded_config.get_pathes_audio_files()
    return []

@_handle_format
@_handle_none
def get_path_to_generated_suite():
    return sys.argv[1]

@_handle_format
@_handle_none
def get_path_to_generated_test():
    from vatf.generator import gen_tests
    test_name = gen_tests.get_test_name()
    if test_name == None:
        raise Exception("None test is processed")
    return os_proxy.join(get_path_to_generated_suite(), test_name)

@_handle_format
@_handle_none
def get_relative_path_to_audio_files_in_test():
    return "assets/audio_files"

@_handle_format
@_handle_none
def get_absolute_path_to_audio_files_in_test():
    test_path = get_path_to_generated_test()
    audio_files_path = get_relative_path_to_audio_files_in_test()
    return os_proxy.join(test_path, audio_files_path)

@_handle_format
@_handle_none
def get_vatf_branch_to_clone():
    global _loaded_config
    return _loaded_config.vatf.branch

@_handle_format
@_handle_none
def get_log_path(session_path):
    global _loaded_config
    if _loaded_config:
        log_path = _loaded_config.get_log_path()
        log_path.format(session_path = session_path)
        return log_path
    return ""

@_handle_format
@_handle_none
def convert_to_log_zone(dt):
    global _loaded_config
    if _loaded_config:
        return _loaded_config.convert_to_log_zone(dt)
    return dt

@_handle_format
@_handle_none
def convert_to_system_zone(dt):
    global _loaded_config
    if _loaded_config:
        return _loaded_config.convert_to_system_zone(dt)
    return dt

@_handle_format
@_handle_none
def get_shell_command():
    global _loaded_config
    if _loaded_config:
        shell_command = _loaded_config.get_shell_command()
        return shell_command
    return None

@_handle_format
@_handle_none
def get_shell_command_restart_timeout():
    global _loaded_config
    if _loaded_config:
        return _loaded_config.get_shell_command_restart_timeout()
    return None
