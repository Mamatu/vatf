from vatf.utils import utils
from vatf.vatf_register import public_api

@public_api("shell")
def command(command):
    os.command(command)
