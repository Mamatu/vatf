from vatf.executor import shell
from vatf.generator import shell

from vatf import vatf_api

def _get_api():
    return vatf_api.get_api("shell")

def command(command):
    _get_api().command(command)
