from random import random
from random import randint
from vatf.generator import gen_tests
from vatf.utils import config

from enum import Enum

def _sleep(t):
    gen_tests.create_call("wait", "sleep", t)

def _sleep_random(t1, t2):
    gen_tests.create_call("wait", "sleep_random", t1, t2)

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
