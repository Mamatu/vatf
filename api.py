from vatf.executor import player
from vatf.generator import player

from vatf import vatf_api

def play_audio(path):
    vatf_api.get_api().play_audio(path)