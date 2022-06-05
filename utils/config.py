import abc
import sys

import logging

from vatf.utils import config_loader, os_proxy

_cfg_loader = None
_cfg_path = None

def _load_config():
    global _cfg_loader, _cfg_path
    if not _cfg_loader:
        path = get_config_path()
        if path:
            _cfg_loader = config_loader.load(path)

def _reset():
    global _cfg_loader, _cfg_path
    _cfg_path = None
    _cfg_loader = None

def set_config_path(path):
    global _cfg_path
    _cfg_path = path

def get_config_path():
    global _cfg_path
    config_path = _cfg_path
    if not config_path and len(sys.argv) > 2:
        config_path = sys.argv[2]
    return config_path

def get_pathes_to_audio_files_in_system():
    _load_config()
    global _cfg_loader
    if _cfg_loader:
        return _cfg_loader.get_pathes_audio_files()
    return []

def get_path_to_generated_suite():
    return sys.argv[1]

def get_relative_path_to_audio_files_in_test():
    return "assets/audio_files"

def get_absolute_path_to_audio_files_in_test():
    test_path = get_path_to_generated_test()
    audio_files_path = get_relative_path_to_audio_files_in_test()
    return os_proxy.join(test_path, audio_files_path)

def get_vatf_branch_to_clone():
    _load_config()
    global _cfg_loader
    if _cfg_loader:
        return _cfg_loader.get_vatf_branch_to_clone()
    return ""

def get_log_path(session_path):
    _load_config()
    global _cfg_loader
    if _cfg_loader:
        log_path = _cfg_loader.get_log_path()
        log_path.format(session_path = session_path)
        return log_path
    return ""

def convert_to_log_zone(dt):
    _load_config()
    global _cfg_loader
    if _cfg_loader:
        return _cfg_loader.convert_to_log_zone(dt)
    return dt

def convert_to_system_zone(dt):
    _load_config()
    global _cfg_loader
    if _cfg_loader:
        return _cfg_loader.convert_to_system_zone(dt)
    return dt

def get_shell_command():
    _load_config()
    global _cfg_loader
    if _cfg_loader:
        shell_command = _cfg_loader.get_shell_command()
        return shell_command
    return None

def get_shell_command_restart_timeout():
    _load_config()
    global _cfg_loader
    if _cfg_loader:
        return _cfg_loader.get_shell_command_restart_timeout()
    return None
