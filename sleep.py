from vatf.executor import sleep
from vatf.generator import sleep

from vatf import vatf_api

def _get_api():
    return vatf_api.get_api("sleep")

def sleep(t):
    _get_api().sleep(t)

def sleep_random(t1, t2):
    _get_api().sleep_random(t1, t2)
