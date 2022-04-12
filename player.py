from vatf.executor import exec_player
from vatf.generator import gen_player

from vatf import vatf_api

def play_audio(path):
    vatf_api.get_api().play_audio(path)
