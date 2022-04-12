"""
Logger module is for extract part of session log which is related to running test case.
It is one of method to collect log data.
"""

import datetime

import time
import logging


import signal
import sys

from vatf.utils import logger_thread
from vatf.utils import utils, os_proxy

_logger_thread = None

def Start(now, inpath, outpath, config_path = None):
    def check_file(path):
        if not os_proxy.exists(path):
            raise FileNotFoundError(path)
    check_file(inpath)
    global _logger_thread
    _logger_thread = logger_thread.LoggerThread(now, inpath, outpath, config_path)
    _logger_thread.start()

def WaitForLine():
    global _logger_thread
    if not _logger_thread:
        raise Exception("Not logger thread")
    _logger_thread.waitForLine()

def Stop():
    global _logger_thread, _finish
    if not _logger_thread:
        raise Exception("Not logger thread")
    _logger_thread.stop()

def main(args):
    if not args.path_to_output_dir:
        raise Exception(f"Lack of {args.path_to_output_dir.__name__}")
    if not args.path_to_input_log:
        raise Exception(f"Lack of {args.path_to_input_log.__name__}")
    if not args.output_file_name:
        args.output_file_name = "session.log"
    import os
    output_path = os.path.join(args.path_to_output_dir, args.output_file_name)
    _now = datetime.datetime.now()
    Start(_now, args.path_to_input_log, output_path)
    def signal_handler(sig, frame):
        Stop()
    signal.signal(signal.SIGINT, signal_handler)
