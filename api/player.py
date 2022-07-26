from vatf import vatf_api
from vatf.utils import utils

def _get_api():
    return vatf_api.get_api("player")

def play_audio(path):
    utils.print_func_info()
    _get_api().play_audio(path)
