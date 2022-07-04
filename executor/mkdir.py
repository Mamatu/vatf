import os
import re

from vatf.utils import utils

import logging

def _mkdir(path):
    os.makedirs(path)

def get_count(path):
    top = os.path.basename(path)
    dir = os.path.dirname(path)
    return utils.get_counter(dir, top) + 1

def get_count_path(path):
    top = os.path.basename(path)
    dir = os.path.dirname(path)
    counter = get_count(path)
    path = f"{os.path.join(dir, top)}_{counter}/"
    return path

def mkdir_with_counter(path):
    path = get_count_path(path)
    os.makedirs(path)
    logging.info(f"{mkdir_with_counter.__name__}: {path}")
    return path
