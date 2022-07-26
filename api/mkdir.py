from vatf import vatf_api
from vatf.utils import utils

def _get_api():
    return vatf_api.get_api("mkdir")

def get_count(path):
    utils.print_func_info()
    return _get_api().get_count(path)

def get_count_path(path):
    utils.print_func_info()
    return _get_api().get_count_path(path)

def mkdir(path):
    utils.print_func_info()
    _get_api().mkdir(path)

def mkdir_with_date(path):
    utils.print_func_info()
    return _get_api().mkdir_with_date(path)

def mkdir_with_counter(path):
    utils.print_func_info()
    return _get_api().mkdir_with_counter(path)
