import time as t
import logging
from random import random
from random import randint

from vatf.utils import utils
from vatf.vatf_register import public_api

@public_api("sleep")
def sleep(duration):
    t.sleep(duration)

@public_api("sleep")
def sleep_random(t1, t2):
    t.sleep(randint(t1, t2))

#
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
