from vatf import vatf_api
import time as t
import logging
from random import random
from random import randint

from vatf.executor import search
from vatf.utils import utils, os_proxy, config_handler

import datetime

@vatf_api.public_api("wait")
def sleep(duration):
    t.sleep(duration)

@vatf_api.public_api("wait")
def sleep_random(t1, t2):
    t.sleep(randint(t1, t2))

def _wait_for_regex_command(regex, timeout = 30, pause = 0.5, **kwargs):
    import vatf.executor.log_snapshot_class as log_snapshot_class
    log_snapshot = log_snapshot_class.make()
    temp_file = utils.get_temp_file()
    temp_filepath = temp_file.name
    print(f"wait_for_regex -> {temp_filepath}")
    try:
        wait_command_key = "wait_for_regex.command"
        command = config_handler.get_var(wait_command_key, **kwargs)
        command = command.format(log_path = temp_filepath)
        log_snapshot.start(log_path = temp_filepath, shell_cmd = command)
        start_point = t.time()
        while True:
            out = search.find(filepath = temp_filepath, regex = regex)
            print(f"len: {len(out)}")
            if len(out) > 0:
                return True
            t.sleep(pause)
            end_point = t.time()
            if (end_point - start_point) > timeout:
                print(f"timeout: {end_point} {start_point}")
                return False
    finally:
        log_snapshot.stop()
        temp_file.close()

def _wait_for_regex_path(regex, timeout = 30, pause = 0.5, **kwargs):
    import vatf.executor.log_snapshot_class as log_snapshot_class
    wait_for_regex_path_key = "wait_for_regex.path"
    wait_for_regex_date_format_key = "wait_for_regex.date_format"
    wait_for_regex_date_regex_key = "wait_for_regex.date_regex"
    wait_path_vars_key = [wait_for_regex_path_key, wait_for_regex_date_format_key, wait_for_regex_date_regex_key]
    output = config_handler.get_vars(wait_path_vars_key, **kwargs)
    log_filepath = output[wait_for_regex_path_key]
    date_format = output[wait_for_regex_date_format_key]
    date_regex = output[wait_for_regex_date_regex_key]
    print(f"wait_for_regex -> {log_filepath}")
    start_point = t.time()
    while True:
        out = search.find(filepath = log_filepath, regex = regex)
        print(f"len: {len(out)}")
        if len(out) > 0:
            return True
        t.sleep(pause)
        end_point = t.time()
        if (end_point - start_point) > timeout:
            print(f"timeout: {end_point} {start_point}")
            return False

@vatf_api.public_api("wait")
def wait_for_regex(regex, timeout = 30, pause = 0.5, **kwargs):
    if config_handler.has_var("wait_for_regex.command", **kwargs):
        return _wait_for_regex_command(regex, timeout = timeout, pause = pause, **kwargs)
    else:
        return _wait_for_regex_path(regex, timeout = timeout, pause = pause, **kwargs)
