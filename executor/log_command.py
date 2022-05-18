"""
Takes the snapshot of log between start and stop method.
"""

import time
import logging

import datetime

from vatf.executor import shell, mkdir
from vatf.vatf_api import public_api

from vatf.utils import logger_thread
from vatf.utils import utils, os_proxy

_logger_thread = None
class _Ctx:
    def __init__(self, now, log_path, config_path, output_path, snapshot_path):
        self.now = now
        self.log_path = log_path
        self.config_path = config_path
        self.snapshot_path = snapshot_path
        self.output_path = output_path

_ctx = None

@public_api("log_snapshot")
def start(log_path, snapshot_path, now = datetime.datetime.now, config_path ="./config.json"):
    global _ctx
    if _ctx:
        raise Exception(f"{start.__name__} Log snapshot is already started!")
    output_path = mkdir.mkdir_with_counter("./logs/session")
    if callable(now): now = now()
    _ctx = _Ctx(now = now, snapshot_path = snapshot_path, config_path = config_path, log_path = log_path, output_path = output_path)

def stop():
    global _ctx
    try:
        if not _ctx:
            raise Exception(f"{stop.__name__} was not called start before!")
        start_line = -1
        end_line = -1
        results = utils.grep_regex_in_line(_ctx.log_path, grep_regex = ".*", match_regex = utils.DATE_REGEX)
        logging.debug(f"{stop.__name__} founds {len(results)} results")
        for result in results:
            dt = datetime.datetime.strptime(result.matched[0], utils.DATE_FORMAT)
            logging.debug(f"{stop.__name__} founds datetime in line {dt} and compares to {_ctx.now}")
            diff = dt - _ctx.now
            logging.debug(f"{stop.__name__} {diff} > {datetime.timedelta()}")
            if diff >= datetime.timedelta():
                if start_line == -1:
                    start_line = result.line_number - 1
                    logging.debug(f"{stop.__name__} found start line {start_line}")
                if end_line == -1 or result.line_number > end_line:
                    end_line = result.line_number
                    logging.debug(f"{stop.__name__} updated end line {end_line}")
        lf_lines = None
        with os_proxy.open_to_read(_ctx.log_path) as lf:
            lf_lines = lf.readlines()
            with os_proxy.open_to_write(_ctx.snapshot_path) as sf:
                lf_lines = lf_lines[start_line : end_line]
                sf.writelines(lf_lines)
        _ctx = None
        return (start_line, end_line)
    finally:
        _ctx = None
