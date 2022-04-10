import os
import shutil
import sys
import uuid
from enum import Enum
from random import random
from random import randint

from vatf.generator import ctx

def WaitForTimeout(timeout):
    ctx.Get().wait_for_timeout(timeout)

def Sleep(timeout):
    WaitForTimeout(timeout)

def SleepRandom(randomRange):
    Sleep(randint(randomRange[0], randomRange[1]))

def WaitForRegex(regex, path_to_log, timeout = 10, delta = 0.5):
    ctx.Get().wait_for_regex(regex, path_to_log, timeout, delta)
