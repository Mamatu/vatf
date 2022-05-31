from random import random
from random import randint
from vatf.generator import gen_tests
from vatf.utils import config

from enum import Enum

class RandomStage(Enum):
    GENERATOR = 1,
    EXECUTOR = 2

def sleep_random(t1, t2, randomStage = RandomStage.GENERATOR):
    if randomStage == RandomStage.GENERATOR:
        t = randint(t1, t2)
        gen_tests.replace_call("wait", "sleep", t, sleep_random)
    elif randomStage == RandomStage.EXECUTOR:
        gen_tests.replace_call("wait", "sleep_random", t1, t2, sleep_random)
    else:
        raise Exception(f"Invalid random stage {randomStage}. Possibilites: {RandomStage}")
