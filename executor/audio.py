from vatf.executor import shell

def record_inputs_outputs():
    global _rec_bg
    filepath = ctx.Get().mkdir_incr("./recordings/session")
    rec_command = f"python vatf_utils/papy.py --recorder=gst --rec --dir $(cat {filepath})"
    shell.bg(rec_command)
