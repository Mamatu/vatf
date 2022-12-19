from vatf import vatf_api
from vatf.utils import utils

def _get_api():
    return vatf_api.get_api("shell")

def fg(command):
    utils.print_func_info()
    _get_api().fg(command)

def bg(command, shell = True):
    utils.print_func_info()
    return _get_api().bg(command, shell)

def kill(process):
    utils.print_func_info()
    _get_api().kill(process)
