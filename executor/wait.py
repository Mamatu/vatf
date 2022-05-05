import time as t
import logging
from random import random
from random import randint

from vatf.utils import utils, os_proxy, config
from vatf.vatf_register import public_api

import datetime

@public_api("wait")
def sleep(duration):
    t.sleep(duration)

@public_api("wait")
def sleep_random(t1, t2):
    t.sleep(randint(t1, t2))

class WfrCallbacks:
    def __init__(self):
        pass
    def success(timestamp, matched):
        pass
    def timeout(timeout):
        pass
    def pre_sleep(time):
        pass

@public_api("wait")
def wait_for_regex(regex, log_path, timeout = 10, pause = 0.5, start_time = None, callbacks = None):
    def convert_to_timedelta(t):
        if not isinstance(t, datetime.timedelta):
            return datetime.timedelta(seconds = t)
        return t
    def call(callbacks, method_name, *args):
        if callbacks:
            method = getattr(callbacks, method_name)
            method(*args)
    def init_log_path(log_path):
        if log_path == None:
            return config.get_log_path()
        return log_path
    def _sleep(time):
        logging.debug(f"{wait_for_regex.__name__}: sleep {time}")
        call(callbacks, "pre_sleep", time)
        if isinstance(time, datetime.timedelta):
            time = time / datetime.timedelta(seconds = 1)
        t.sleep(time)
    if start_time == None:
        start_time = datetime.datetime.now()
    log_path = init_log_path(log_path)
    if not os_proxy.exists(log_path):
        raise FileNotFoundError(log_path)
    pause = convert_to_timedelta(pause)
    timeout = convert_to_timedelta(timeout)
    start_real_time = datetime.datetime.now()
    start_log_time = config.convert_to_log_zone(start_time)
    logging.debug(f"start_time: {start_time} start_log_time: {start_log_time}")
    def calc_delta_time():
        now = datetime.datetime.now()
        diff = now - start_real_time
        return diff
    while True:
        out = utils.grep_regex_in_line(log_path, regex, f"({utils.TIMESTAMP_REGEX}).*({regex})")
        if len(out) > 0:
            matched = out[-1].matched
            regex_timestamp = datetime.datetime.strptime(matched[1], utils.TIMESTAMP_FORMAT)
            logging.debug(f"{wait_for_regex.__name__}: found {len(out)} matches")
            if regex_timestamp >= start_log_time:
                logging.debug(f"{wait_for_regex.__name__}: break {regex_timestamp} > {start_log_time}")
                call(callbacks, "success", regex_timestamp, matched[2])
                return
        diff = calc_delta_time()
        if pause:
            if not diff + pause >= timeout:
                _sleep(pause)
            else:
                pause_timeout = timeout - diff
                _sleep(pause_timeout)
        diff = calc_delta_time()
        if diff > timeout:
            call(callbacks, "timeout", timeout)
            logging.debug(f"{wait_for_regex.__name__}: break {diff} > {timeout} timeout")
            return

#def SleepUntilTimeout(timeout):
#    if isinstance(timeout, str):
#        timeout = int(timeout)
#    logging.info(f"{SleepUntilTimeout.__name__}: {timeout}")
#    t.sleep(timeout)
#
#def _convert_to_utc(date):
#    if config.log_timestamp_in_utc:
#        return utils.convert_to_utc(date)
#    return date
#
#def SleepUntilRegex(regex, path_to_log, timeout = 10, delta_time = 0.5):
#    logging.info(f"{SleepUntilRegex.__name__}: {regex} {path_to_log} {timeout} {delta_time}")
#    if not os.path.exists(path_to_log):
#        raise Exception(f"{path_to_log} does not exist")
#    if delta_time == None:
#        delta_time = 0.5
#    import  datetime
#    start_function_timestamp = _convert_to_utc(datetime.datetime.now())
#    logging.info(f"{SleepUntilRegex.__name__}: function start timestamp {start_function_timestamp}")
#    time_idx = 0
#    while True:
#        out = utils.grep_regex_in_line(path_to_log, regex, utils.TIMESTAMP_REGEX)
#        if len(out) > 0:
#            regex_timestamp = datetime.datetime.strptime(out[-1].matched[0], utils.TIMESTAMP_FORMAT)
#            logging.info(f"{SleepUntilRegex.__name__}: found {len(out)} matches")
#            if regex_timestamp >= start_function_timestamp:
#                logging.info(f"{SleepUntilRegex.__name__}: {regex_timestamp} > {start_function_timestamp} --break")
#                break
#        if delta_time != None:
#            logging.info(f"{SleepUntilRegex.__name__}: sleep on {delta_time}")
#            t.sleep(delta_time)
#            time_idx = time_idx + delta_time
#        if timeout != None:
#            if time_idx >= timeout:
#                logging.info(f"{SleepUntilRegex.__name__}: timeout {timeout} reached --break")
#                break
#def main(args):
#    if args.regex:
#        SleepUntilRegex(regex = args.regex, timeout = args.timeout, delta_time = args.delta, path_to_log = args.path_to_log)
#    elif args.timeout:
#        SleepUntilTimeout(args.timeout)
