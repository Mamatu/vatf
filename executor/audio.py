from vatf.api import shell, mkdir

from vatf import vatf_api
from vatf.utils import config_handler, utils
import logging

@vatf_api.public_api("audio")
def record_inputs_outputs():
    print(f"{record_inputs_outputs.__name__}: {utils.name_and_args()}")
    output_path = mkdir.mkdir_with_counter("./recordings/session")
    rec_command = f"python3 vatf/utils/papy.py --recorder=gst --rec --dir {output_path}"
    logging.debug(f"{record_inputs_outputs.__name__}: {rec_command}")
    shell.bg(rec_command)

@vatf_api.public_api("audio")
def record_inputs_outputs_from_config(**kwargs):
    print(f"{record_inputs_outputs_from_config.__name__}: {utils.name_and_args()}")
    audio_dir_path_key = "audio.path"
    output = config_handler.handle([audio_dir_path_key], **kwargs)
    output_path = output[audio_dir_path_key]
    print(f"output_path: {output_path}")
    mkdir.mkdir(output_path)
    rec_command = f"python3 vatf/utils/papy.py --recorder=gst --rec --dir {output_path}"
    logging.debug(f"{record_inputs_outputs_from_config.__name__}: {rec_command}")
    shell.bg(rec_command)
