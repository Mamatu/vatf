from vatf.executor import mkdir
from vatf.generator import mkdir

from vatf import vatf_api

def _get_api():
    return vatf_api.get_api("mkdir")

def mkdir(path):
    _get_api().mkdir(path)

def mkdir_with_counter(path):
    _get_api().mkdir_with_counter(path)
