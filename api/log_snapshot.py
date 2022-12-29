__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

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
