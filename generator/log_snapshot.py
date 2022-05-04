from vatf.generator import gen_tests

def start(path_to_log):
    gen_tests.create_call("log_snapshot", "start", path_to_log = path_to_log)

def stop():
    gen_tests.create_call("log_snapshot", "stop")
