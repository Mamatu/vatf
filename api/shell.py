from vatf.utils import utils
import logging
import os
import psutil
import subprocess

import atexit
from threading import RLock
from vatf.utils.thread import lock


_popens = []

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

def kill(process):
    if _check_and_unregister(process):
        parent = psutil.Process(process.pid)
        children = parent.children(recursive=True)
        for child in children:
            child.kill()
        process.terminate()
        logging.debug(f"Killed children and terminated process {process.pid}")
        process.wait()

def bg(command):
    process = subprocess.Popen(command, shell=True)
    logging.debug(f"Run process {process.pid} in background for command {command}")
    _register_process(process)
    atexit.register(kill, process)
    return process
