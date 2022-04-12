from vatf.generator import gen_tests

def _mkdir(path):
    gen_tests.create_call("mkdir", path = path)

def _getTempFileName():
    import tempfile
    return tempfile.NamedTemporaryFile().name

def MkdirIncr(path):
    filepath = _getTempFileName()
    ctx.Get().writeExecutor(f"mkdir --path_to_counter {path} --output_save_to {filepath}")
    return filepath
