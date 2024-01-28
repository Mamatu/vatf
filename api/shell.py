__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from vatf import vatf_api
from vatf.utils import utils

def _get_api():
    return vatf_api.get_api("shell")

def fg(command, shell = True, stderr_exception = True):
    utils.print_func_info()
    _get_api().fg(command, shell, stderr_exception)

def bg(command, shell = True):
    utils.print_func_info()
    return _get_api().bg(command, shell)

def kill(process):
    utils.print_func_info()
    _get_api().kill(process)
