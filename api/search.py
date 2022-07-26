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
