from vatf.generator import ctx

def _getTempFileName():
    import tempfile
    return tempfile.NamedTemporaryFile().name

def MkdirIncr(path):
    filepath = _getTempFileName()
    ctx.Get().writeExecutor(f"mkdir --path_to_counter {path} --output_save_to {filepath}")
    return filepath
