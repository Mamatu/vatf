from vatf.utils import utils
from vatf.vatf_register import public_api
import logging
import os
import psutil
import subprocess

import atexit

_popens = []

@public_api("shell")
def fg(command):
    os.system(command)

@public_api("shell")
def bg(command):
    process = subprocess.Popen(command, shell=True)
    logging.debug(f"Run process {process.pid} in background")
    def on_exit(process):
        parent = psutil.Process(process.pid)
        children = parent.children(recursive=True)
        for child in children:
            child.kill()
        process.terminate()
        logging.debug(f"Killed and terminated process {process.pid} with children")
        process.wait()
    atexit.register(on_exit, process)
