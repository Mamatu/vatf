from vatf.generator import config, gen_tests

def _command(command):
    gen_tests.create_call("shell", "command", command)

def command(command):
    _command(command)
