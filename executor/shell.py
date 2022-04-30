from vatf.utils import utils
from vatf.vatf_register import public_api
import os
import subprocess

import atexit

_popens = []

@public_api("shell")
def fg(command):
    os.system(command)

@public_api("shell")
def bg(command):
    command = command.split(" ")
    process = subprocess.Popen(command, shell=True)
    def on_exit(process):
        process.terminate()
        process.wait()
    atexit.register(on_exit, process)
