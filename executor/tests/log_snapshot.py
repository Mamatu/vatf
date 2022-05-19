from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import errno
import datetime
import logging
import textwrap
import time
import threading
import os

import sys

from vatf.executor import log_snapshot
from vatf.utils import utils, config

_counter = None
def _log_generator(filepath, lines):
    global _counter
    if not _counter:
        _counter = 0
    while _counter <= lines:
        log_line = f"line{_counter + 1}"
        now = datetime.datetime.now()
        line = f"{now} {log_line}\n"
        log_file = open(filepath, "a")
        log_file.write(line)
        log_file.flush()
        log_file.close()
        time.sleep(0.0001)
        _counter = _counter + 1

def _log_generator_thread(filepath, lines):
    t = threading.Thread(target = _log_generator, args = (filepath,lines,))
    t.start()
    return t

class LogSnapshotTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    def setUp(self):
        from vatf.utils import config
        config._reset()
    def create_file(self, mode, data = None):
        path = utils.get_temp_filepath()
        with open(path, mode) as f:
            if data:
                if isinstance(data, str):
                    f.write(data)
                if isinstance(data, list):
                    f.writelines(data)
        return path
    def test_log_with_timestamps(self):
        log_path = utils.get_temp_filepath()
        log_path_1 = utils.get_temp_filepath()
        t = _log_generator_thread(log_path, 2253)
        utils.touch(log_path_1)
        log_snapshot.start(log_path_1, f"while true; do bash -c \"cat {log_path} >> {log_path_1}; sync\"; sleep 0.01; done", 10)
        time.sleep(1)
        with open(log_path_1, "r") as f:
            self.assertTrue(2253, len(f.readlines()))
        t.join()
