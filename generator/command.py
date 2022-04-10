import os
import shutil
import sys
import uuid
from enum import Enum
from random import random
from random import randint

from vatf.generator import ctx
from pysh.bash import bg
from pysh.core import Command as PyshCommand

def RunBg(command, signal = "SIGINT"):
    process = bg.BackgroundProcess(command, signal)
    process.launch()()
    return process

def Kill(process):
    """
    Kill process

    :param process: process to kill
    """
    process.kill()()

def KillBg(process):
    """
    Alias for Kill

    :param process: process to kill
    """
    Kill(process)

def Run(command):
    cmd = PyshCommand()
    cmd.cmdStr(command)
    cmd.cmdNL()
    cmd()
