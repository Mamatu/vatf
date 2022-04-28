from random import random
from random import randint
from vatf.generator import config, gen_tests

def _sleep(t):
    gen_tests.create_call("sleep", "sleep", t)

def _sleep_random(t1, t2):
    gen_tests.create_call("sleep", "sleep_random", t1, t2)

def sleep(t):
    _sleep(t)

def sleep_random(t1, t2):
    _sleep(randint(t1, t2))

#def WaitForTimeout(timeout):
#    ctx.Get().wait_for_timeout(timeout)
#
#def Sleep(timeout):
#    WaitForTimeout(timeout)
#
#def SleepRandom(randomRange):
#    Sleep(randint(randomRange[0], randomRange[1]))
#
#def WaitForRegex(regex, path_to_log, timeout = 10, delta = 0.5):
#    ctx.Get().wait_for_regex(regex, path_to_log, timeout, delta)
