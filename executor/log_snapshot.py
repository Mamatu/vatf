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

from vatf.executor import log_snapshot_class, mkdir
from vatf.utils import config_handler, os_proxy

_log_snapshot = None

@vatf_api.public_api("log_snapshot")
def start(log_path, shell_cmd, monitorFileLines = True):
    global _log_snapshot
    if _log_snapshot:
        raise Exception("log_snapshot.start was already invoked!")
    _log_snapshot = log_snapshot_class.make()
    _log_snapshot.start(log_path = log_path, shell_cmd = shell_cmd, monitorFileLines = monitorFileLines)

@vatf_api.public_api("log_snapshot")
def start_from_config(monitorFileLines = True, **kwargs):
    log_command_key = "va_log.command"
    log_path_key = "va_log.path"
    output = config_handler.handle([log_command_key, log_path_key], **kwargs)
    shell_cmd = output[log_command_key]
    log_path = output[log_path_key]
    mkdir.mkdir(os_proxy.dirname(log_path))
    start(log_path, shell_cmd)

@vatf_api.public_api("log_snapshot")
def stop():
    global _log_snapshot
    if _log_snapshot:
        _log_snapshot.stop()
        _log_snapshot = None

import atexit
atexit.register(stop)
