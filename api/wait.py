from vatf import vatf_api
from vatf.utils import utils

def _get_api():
    return vatf_api.get_api("wait")

def sleep(t):
    utils.print_func_info()
    _get_api().sleep(t)

def sleep_random(t1, t2):
    utils.print_func_info()
    _get_api().sleep_random(t1, t2)

def wait_for_regex(regex, timeout, pause):
    utils.print_func_info()
    return _get_api().wait_for_regex(regex, timeout, pause)
