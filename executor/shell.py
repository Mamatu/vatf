from vatf.utils import utils
from vatf.vatf_register import public_api
import os

@public_api("shell")
def command(command):
    os.system(command)
