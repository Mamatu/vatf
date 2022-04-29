from vatf.executor import shell, mkdir
from vatf.vatf_register import public_api

@public_api("audio")
def record_inputs_outputs():
    global _rec_bg
    mkdir.mkdir_with_counter("./recordings/session")
    rec_command = f"python vatf_utils/papy.py --recorder=gst --rec --dir $(cat {filepath})"
    shell.bg(rec_command)
