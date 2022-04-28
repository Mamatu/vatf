from vatf.executor import player
from vatf.generator import player

from vatf import vatf_api

def _get_api():
    return vatf_api.get_api("player")

def play_audio(path):
    _get_api().play_audio(path)
