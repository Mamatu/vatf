from vatf import vatf_api
from vatf.utils import utils
import logging
import os
import psutil
import subprocess

import atexit
from threading import RLock
from vatf.utils.thread import lock

_popens = []

@vatf_api.public_api("shell")
def fg(command):
    os.system(command)

_active_processes = set()
_mutex = RLock()

@lock(_mutex)
def _register_process(process):
    global _active_processes
    _active_processes.add(process)

@lock(_mutex)
def _is_registered(process):
    global _active_processes
    return process in _active_processes

@lock(_mutex)
def _check_and_unregister(process):
    global _active_processes
    reg = _is_registered(process)
    if reg:
        _unregister_process(process)
    return reg

@lock(_mutex)
def _unregister_process(process):
    global _active_processes
    _active_processes.remove(process)

@vatf_api.public_api("shell")
def kill(process):
    if _check_and_unregister(process):
        parent = psutil.Process(process.pid)
        children = parent.children(recursive=True)
        for child in children:
            try:
                child.kill()
            except psutil.NoSuchProcess as nsp:
                logging.warn(nsp)
        process.terminate()
        logging.debug(f"Killed children and terminated process {process.pid}")
        process.wait()

@vatf_api.public_api("shell")
def bg(command, shell = True):
    process = subprocess.Popen(command, shell = shell)
    logging.debug(f"Run process {process.pid} in background for command {command}")
    _register_process(process)
    atexit.register(kill, process)
    return process
