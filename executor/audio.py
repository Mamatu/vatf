from vatf.api import shell, mkdir

from vatf import vatf_api
from vatf.utils import config_handler, utils
import logging


_processes = []

@vatf_api.public_api("audio")
def record_inputs_outputs():
    global _processes
    output_path = mkdir.mkdir_with_counter("./recordings/session")
    rec_command = f"python3 vatf/utils/papy.py --recorder=gst --rec --dir {output_path}"
    logging.debug(f"{record_inputs_outputs.__name__}: {rec_command}")
    _processes.append(shell.bg(rec_command))

@vatf_api.public_api("audio")
def record_inputs_outputs_from_config(**kwargs):
    global _processes
    audio_dir_path_key = "audio.path"
    output = config_handler.handle([audio_dir_path_key], **kwargs)
    output_path = output[audio_dir_path_key]
    print(f"output_path: {output_path}")
    mkdir.mkdir(output_path)
    rec_command = f"python3 vatf/utils/papy.py --recorder=gst --rec --dir {output_path}"
    logging.debug(f"{record_inputs_outputs_from_config.__name__}: {rec_command}")
    _processes.append(shell.bg(rec_command))


def stop():
    global _processes
    for p in _processes:
        shell.kill(p)
    _processes.clear()
