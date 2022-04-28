from vatf.generator import gen_tests

def mkdir(path):
    gen_tests.create_call("mkdir", "mkdir", path)

def mkdir_with_counter(path):
    gen_tests.create_call("mkdir", "mkdir_with_counter", path)
