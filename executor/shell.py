from vatf.utils import utils
from vatf.vatf_api import public_api
import logging
import os
import psutil
import subprocess

import atexit

_popens = []

@public_api("shell")
def fg(command):
    os.system(command)

def kill(process):
    parent = psutil.Process(process.pid)
    children = parent.children(recursive=True)
    for child in children:
        child.kill()
    process.terminate()
    logging.debug(f"Killed and terminated process {process.pid} with children")
    process.wait()

@public_api("shell")
def bg(command):
    process = subprocess.Popen(command, shell=True)
    logging.debug(f"Run process {process.pid} in background for command {command}")
    atexit.register(kill, process)
    return process
