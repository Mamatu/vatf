from vatf.api import shell, mkdir

from vatf import vatf_api
import logging

@vatf_api.public_api("audio")
def record_inputs_outputs():
    output_path = mkdir.mkdir_with_counter("./recordings/session")
    rec_command = f"python3 vatf/utils/papy.py --recorder=gst --rec --dir {output_path}"
    logging.debug(f"{record_inputs_outputs.__name__}: {rec_command}")
    shell.bg(rec_command)
