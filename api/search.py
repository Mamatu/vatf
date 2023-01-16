__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from vatf import vatf_api
from vatf.utils import utils

def _get_api():
    return vatf_api.get_api("search")

def find(regex, filepath = None, only_math = False):
    utils.print_func_info()
    return _get_api().find(regex, filepath = filepath, only_match = only_match)

def contains(regex, filepath = None):
    utils.print_func_info()
    return _get_api().contains(regex, filepath = filepath)

def find_in_line(grep_regex, match_regex, filepath = None):
    utils.print_func_info()
    return _get_api().find_in_line(grep_regex, match_regex, filepath = filepath)
