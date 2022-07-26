from vatf import vatf_api

import time as t
import logging
from random import random
from random import randint

from vatf.utils import utils, os_proxy, config_handler

import datetime

_va_log_path = "va_log.path"

def _get_log_path(filepath, **kwargs):
    if filepath is None:
        global _va_log_path
        outcome = config_handler.handle([_va_log_path], **kwargs)
        filepath = outcome[_va_log_path]
        return filepath
    return filepath

@vatf_api.public_api("search")
def find(regex, filepath = None, only_match = False, **kwargs):
    filepath = _get_log_path(filepath, **kwargs)
    return utils.grep(filepath, regex, onlyMatch = only_match)

@vatf_api.public_api("search")
def contains(regex, filepath = None, **kwargs):
    outcome = find(regex, filepath = filepath, **kwargs)
    return len(outcome) > 0

@vatf_api.public_api("search")
def find_in_line(grep_regex, match_regex, filepath = None, **kwargs):
    filepath = _get_log_path(filepath, **kwargs)
    return utils.grep_in_line(filepath, grep_regex = grep_regex, match_regex = match_regex)
