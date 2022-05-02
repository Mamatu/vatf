import abc
import sys

import logging

from vatf.utils import config_loader, os_proxy

_cfg_loader = None
_cfg_path = None

def _load_config():
    global _cfg_loader, _cfg_path
    if not _cfg_loader:
        _cfg_loader = config_loader.load(get_config_path())

def set_config_path(path):
    global _cfg_path
    _cfg_path = path

def get_config_path():
    global _cfg_path
    config_path = _cfg_path
    if not config_path:
        config_path = sys.argv[2]
    return config_path

def get_pathes_to_audio_files_in_system():
    _load_config()
    global _cfg_loader
    return _cfg_loader.get_pathes_audio_files()

def get_path_to_generated_suite():
    return sys.argv[1]

def get_path_to_generated_test():
    from vatf.generator import gen_tests
    test_name = gen_tests.get_test_name()
    if test_name == None:
        raise Exception("None test is processed")
    return os_proxy.join(get_path_to_generated_suite(), test_name)

def get_relative_path_to_audio_files_in_test():
    return "assets/audio_files"

def get_absolute_path_to_audio_files_in_test():
    test_path = get_path_to_generated_test()
    audio_files_path = get_relative_path_to_audio_files_in_test()
    return os_proxy.join(test_path, audio_files_path)

def get_vatf_branch_to_clone():
    _load_config()
    global _cfg_loader
    return _cfg_loader.get_vatf_branch_to_clone()
