from vatf.utils import utils
from vatf.vatf_register import public_api
import os
import subprocess

@public_api("shell")
def fg(command):
    os.command(command)

@public_api("shell")
def bg(command):
    command = command.split(" ")
    subprocess.Popen(command)
