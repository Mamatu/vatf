from vatf import vatf_api
import subprocess
import logging

from vatf.utils import os_proxy, utils

def _cvlc_command(path):
    return f"cvlc {path} --play-and-exit vlc://quit"

def cvlc_play_audio(path):
    path = os_proxy.join("assets/audio_files/", path)
    command = _cvlc_command(path)
    logging.info(f"{cvlc_play_audio.__name__}: {command}")
    proc = subprocess.Popen(command, shell=True)
    proc.wait()

def load_audio_files(**kwargs):
    import os
    from vatf.utils import config_handler
    config = config_handler.get_config(**kwargs)
    audio_configs = config.assets
    if isinstance(audio_configs, str):
        audio_configs = [audio_configs]
    for audio_config in audio_configs:
        path = audio_config.path
        files = os.listdir(path)


@vatf_api.public_api("player")
def play_audio(*args, **kwargs):
    if "path" in kwargs:
        cvlc_play_audio(kwargs["path"])
    else:
        cvlc_play_audio(args[0])
