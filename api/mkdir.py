import os
import re

from vatf.utils import utils
from vatf.vatf_api import public_api

import logging

@public_api("mkdir")
def _mkdir(path):
    os.makedirs(path)

@public_api("mkdir")
def mkdir_with_counter(path):
    top = os.path.basename(path)
    dir = os.path.dirname(path)
    counter = utils.get_counter(dir, top) + 1
    path = f"{os.path.join(dir, top)}_{counter}/"
    os.makedirs(path)
    logging.info(f"{mkdir_with_counter.__name__}: {path}")
    return path
