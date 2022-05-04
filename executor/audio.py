from vatf.executor import shell, mkdir
from vatf.vatf_register import public_api

import logging

@public_api("audio")
def record_inputs_outputs():
    output_path = mkdir.mkdir_with_counter("./recordings/session")
    rec_command = f"python3 vatf/utils/papy.py --recorder=gst --rec --dir {output_path}"
    logging.debug(f"{record_inputs_outputs.__name__}: {rec_command}")
    shell.bg(rec_command)
