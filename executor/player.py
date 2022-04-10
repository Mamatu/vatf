import subprocess
import logging

from vatf.test_api import test_api

def _get_command(path):
    return f"cvlc {path} --play-and-exit vlc://quit"

def cvlc_play_audio(path):
    command = _get_command(path)
    logging.info(f"{cvlc_play_audio.__name__}: {command}")
    proc = subprocess.Popen(command, shell=True)
    proc.wait()

@test_api
def play_audio(*args, **kwargs):
    cvlc_play_audio(kwargs["path"])
