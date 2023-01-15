__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from vatf import vatf_api
from vatf.utils import utils

import atexit
import subprocess

class StderrException(Exception):
    pass

@vatf_api.public_api("shell")
def fg(command, shell = True):
    def read_output(output):
        lines = []
        for line in output:
            lines.append(line.decode('utf-8').replace("\n", ""))
        output.close()
        return lines
    process = subprocess.Popen(command, shell = shell, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    process.wait()
    lines = read_output(process.stderr)
    if len(lines) > 0:
        lines = "\n".join(lines)
        raise StderrException(f"Stderr from {command}: {lines}")
    lines = read_output(process.stdout)
    return "\n".join(lines)

@vatf_api.public_api("shell")
def bg(command, shell = True):
    process = subprocess.Popen(command, shell = shell)
    logging.debug(f"Run process {process.pid} in background for command {command}")
    _register_process(process)
    atexit.register(kill, process)
    return process

import logging
import psutil

from threading import RLock
from vatf.utils.thread import lock

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
