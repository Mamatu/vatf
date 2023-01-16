__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

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

def wait_for_regex(regex, timeout, pause, **kwargs):
    utils.print_func_info()
    return _get_api().wait_for_regex(regex, timeout, pause, **kwargs)
