import os
import re

from vatf.utils import utils

import logging

def _mkdir(path):
    os.makedirs(path)

def mkdir_with_counter(path):
    top = os.path.basename(path)
    dir = os.path.dirname(path)
    counter = utils.get_counter(dir, top) + 1
    path = f"{os.path.join(dir, top)}_{counter}/"
    os.makedirs(path)
    logging.info(f"{mkdir_with_counter.__name__}: {path}")
    return path
