from vatf import vatf_api

import time as t
import logging
from random import random
from random import randint

from vatf.utils import utils, os_proxy, config

import datetime

@vatf_api.public_api("search")
def find(filepath, regex):
    return utils.grep(filepath, regex)

@vatf_api.public_api("search")
def find_in_line(filepath, grep_regex, match_regex):
    return utils.grep_in_line(filepath, grep_regex = grep_regex, match_regex = match_regex)
