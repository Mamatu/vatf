from vatf import vatf_api
from vatf.utils import utils

def _get_api():
    return vatf_api.get_api("log_snapshot")

def start(log_path, shell_cmd):
    utils.print_func_info()
    _get_api().start(log_path, shell_cmd)

def start_from_config():
    utils.print_func_info()
    _get_api().start_from_config()

def stop():
    utils.print_func_info()
    _get_api().stop()
