__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from vatf.api import shell, mkdir

from vatf import vatf_api
from vatf.utils import config_handler, utils
import logging

_processes = []

@vatf_api.public_api("audio")
def record_inputs_outputs_from_config(**kwargs):
    global _processes
    audio_dir_path_key = "audio.path"
    config = config_handler.get_config(**kwargs)
    output_path = config.audio.path
    date_format = config.audio.date_format
    date_linux_date_format = config.audio.date_linux_date_format
    print(f"output_path: {output_path}")
    mkdir.mkdir(output_path)
    rec_command = f"python3 vatf/utils/papy.py --recorder=gst --rec --dir {output_path} --date_format='{date_format}' --date_linux_date_format='{date_linux_date_format}'"
    logging.debug(f"{record_inputs_outputs_from_config.__name__}: {rec_command}")
    _processes.append(shell.bg(rec_command))


def stop():
    global _processes
    for p in _processes:
        shell.kill(p)
    _processes.clear()
