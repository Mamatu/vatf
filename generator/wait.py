from random import random
from random import randint
from vatf.generator import gen_tests
from vatf.utils import config

from enum import Enum

def _sleep(t):
    gen_tests.create_call("wait", "sleep", t)

def _sleep_random(t1, t2):
    gen_tests.create_call("wait", "sleep_random", t1, t2)

def sleep(t):
    _sleep(t)

class RandomStage(Enum):
    GENERATOR = 1,
    EXECUTOR = 2

def sleep_random(t1, t2, randomStage = RandomStage.GENERATOR):
    if randomStage == RandomStage.GENERATOR:
        _sleep(randint(t1, t2))
    elif randomStage == RandomStage.EXECUTOR:
        _sleep_random(t1, t2)
    else:
        raise Exception(f"Invalid random stage {randomStage}. Possibilites: {RandomStage}")

def wait_for_regex(regex, log_path, timeout = 10, pause = 0.5):
    gen_tests.create_call("wait", "wait_for_regex", regex, log_path, timeout = timeout, pause = pause)
