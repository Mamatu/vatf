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

def _get_strategy(**kwargs):
    is_command = config_handler.contains("wait_for_regex.command")
    is_path = config_handler.contains("wait_for_regex.path")
    if is_command and is_path:
        raise Exception("Cannot be definded path and command simultaneously")
    if is_command: return "custom_command"
    if is_path: return "custom_path"
    raise Exception("Not command, not path defined")

def wait_for_regex_custom_command(regex, timeout = 30, pause = 0.5, **kwargs):
    import vatf.api.log_snapshot as log_snapshot
    temp_filepath = utils.get_temp_filepath()
    print(f"wait_for_regex -> {temp_filepath}")
    try:
        va_log_command_key = "wait_for_regex.command"
        output = config_handler.handle([va_log_command_key], **kwargs)
        command = output[va_log_command_key]
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
        os_proxy.remove_file(temp_filepath)

@vatf_api.public_api("wait")
def wait_for_regex(regex, timeout = 30, pause = 0.5, **kwargs):
    now = datetime.datetime.now()
    strategy = _get_strategy(**kwargs)
    if strategy == "custom_command":
        return wait_for_regex_custom_command(regex, timeout, pause, **kwargs)
    if strategy == "custom_path":
