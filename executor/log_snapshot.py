__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

"""
Takes the snapshot of log between start and stop method.
"""
from vatf import vatf_api
import logging

from vatf.executor import lib_log_snapshot, mkdir
from vatf.utils import config_handler, os_proxy

_log_snapshot = None

def check_if_invoked():
    global _log_snapshot
    if _log_snapshot:
        raise Exception("log_snapshot.start was already invoked!")

@vatf_api.public_api("log_snapshot")
def start(log_path, shell_cmd):
    return start_cmd(log_path, shell_cmd)

@vatf_api.public_api("log_snapshot")
def start_from_config(**kwargs):
    log_command_key = "va_log.command"
    log_path_key = "va_log.path"
    in_log_path_key = "va_log.in_path"
    config = config_handler.get_config(**kwargs)
    cmd_mode = False
    copy_mode = False
    try:
        cmd_mode = config[log_command_key] and config[log_path_key]
    except KeyError:
        pass
    try:
        copy_mode = config[in_log_path_key] and config[log_path_key]
    except KeyError:
        pass
    if cmd_mode and copy_mode:
        raise Exception("Config fullfil both modes copy and cmd. One is required")
    if not cmd_mode and not copy_mode:
        raise Exception("Config does not contain information to choose mode")
    if cmd_mode:
        return start_cmd_from_config(**kwargs)
    elif copy_mode:
        return start_copy_from_config(**kwargs)
    else:
        raise Exception("Not supported mode")

@vatf_api.public_api("log_snapshot")
def start_cmd(log_path, shell_cmd):
    check_if_invoked()
    _log_snapshot = lib_log_snapshot.make()
    _log_snapshot.start_cmd(log_path = log_path, shell_cmd = shell_cmd)

@vatf_api.public_api("log_snapshot")
def start_cmd_from_config(**kwargs):
    log_command_key = "va_log.command"
    log_path_key = "va_log.path"
    config = config_handler.get_config(**kwargs)
    shell_cmd = config[log_command_key]
    log_path = config[log_path_key]
    mkdir.mkdir(os_proxy.dirname(log_path))
    start_cmd(log_path, shell_cmd)

@vatf_api.public_api("log_snapshot")
def start_copy(log_path, in_log_path):
    check_if_invoked()
    _log_snapshot = lib_log_snapshot.make()
    _log_snapshot.start_copy(log_path = log_path, in_log_path = in_log_path)

@vatf_api.public_api("log_snapshot")
def start_copy_from_config(**kwargs):
    in_log_path_key = "va_log.in_path"
    log_path_key = "va_log.path"
    config = config_handler.get_config(**kwargs)
    in_log_path = config[in_log_path_key]
    log_path =config[log_path_key]
    mkdir.mkdir(os_proxy.dirname(log_path))
    start_copy(log_path, in_log_path)

@vatf_api.public_api("log_snapshot")
def stop():
    global _log_snapshot
    if _log_snapshot:
        _log_snapshot.stop()
        _log_snapshot = None

import atexit
atexit.register(stop)
