from vatf.generator import config, gen_tests

def fg(command):
    gen_tests.create_call("shell", "fg", command)

def bg(command):
    gen_tests.create_call("shell", "bg", command)
