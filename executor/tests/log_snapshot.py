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
_generated_lines = []

def _reset():
    global _counter, _generated_lines
    _counter = None
    _generated_lines = []

def _log_generator(filepath, lines_count):
    global _counter, _generated_lines
    if not _counter:
        _counter = 0
    while _counter < lines_count:
        log_line = f"line{_counter + 1}"
        now = datetime.datetime.now()
        line = f"{now} {log_line}\n"
        _generated_lines.append(line)
        log_file = open(filepath, "a")
        log_file.write(line)
        log_file.flush()
        log_file.close()
        _counter = _counter + 1
        time.sleep(0.0001)

def _log_generator_thread(filepath, lines):
    t = threading.Thread(target = _log_generator, args = (filepath,lines,))
    t.start()
    return t

class LogSnapshotTests(TestCase):
    def __init__(self, arg):
        TestCase.__init__(self, arg)
    def setUp(self):
        from vatf.utils import config
        logging.getLogger().setLevel(logging.INFO)
        config._reset()
        _reset()
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
        global _generated_lines
        log_path = utils.get_temp_filepath()
        log_path_1 = utils.get_temp_filepath()
        lines_count = 2253
        t = _log_generator_thread(log_path, lines_count)
        utils.touch(log_path_1)
        log_snapshot.start(log_path_1, f"while true; do bash -c \"cat {log_path} > {log_path_1}; sync\"; done", 10)
        time.sleep(1)
        t.join()
        with open(log_path_1, "r") as f:
            rlines = f.readlines()
            self.assertEqual(lines_count, len(rlines))
            self.assertEqual(lines_count, len(_generated_lines))
            for idx in range(len(rlines)):
                self.assertEqual(rlines[idx], _generated_lines[idx])
