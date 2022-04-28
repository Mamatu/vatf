import subprocess
import logging

from vatf.vatf_register import public_api

def _cvlc_command(path):
    return f"cvlc {path} --play-and-exit vlc://quit"

def cvlc_play_audio(path):
    command = _cvlc_command(path)
    logging.info(f"{cvlc_play_audio.__name__}: {command}")
    proc = subprocess.Popen(command, shell=True)
    proc.wait()

@public_api(__name__)
def play_audio(*args, **kwargs):
    if "path" in kwargs:
        cvlc_play_audio(kwargs["path"])
    else:
        cvlc_play_audio(args[0])
