from unittest import TestCase
from unittest.mock import Mock, call
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

def _log_generator(filepath, lines_count, custom_sleep = None):
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
        if custom_sleep and _counter in custom_sleep:
            time.sleep(custom_sleep[_counter])
        _counter = _counter + 1

def _log_generator_thread(filepath, lines, custom_sleep = None):
    t = threading.Thread(target = _log_generator, args = (filepath, lines, custom_sleep,))
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
        print("pre test_log_with_timestamps")
        log_path = utils.get_temp_filepath()
        log_path_1 = utils.get_temp_filepath()
        logging.info(f"{log_path} -> {log_path_1}")
        lines_count = 1113
        utils.touch(log_path)
        utils.touch(log_path_1)
        t = _log_generator_thread(log_path, lines_count)
        t.start()
        log_snapshot.start(log_path_1, f"while true; do bash -c \"cat {log_path} > {log_path_1}; sync\"; done", 500)
        t.join()
        time.sleep(0.5)
        log_snapshot.stop()
        with open(log_path_1, "r") as f:
            rlines = f.readlines()
            self.assertEqual(lines_count, len(rlines))
            self.assertEqual(lines_count, len(_generated_lines))
            for idx in range(len(rlines)):
                self.assertEqual(rlines[idx], _generated_lines[idx])
        print("post test_log_with_timestamps")
    @patch("vatf.executor.log_snapshot._restart_command")
    def test_log_with_timestamps_timeout(self, _restart_command):
        global _generated_lines
        print("pre test_log_with_timestamps_timeout")
        log_path = utils.get_temp_filepath()
        log_path_1 = utils.get_temp_filepath()
        logging.info(f"{log_path} -> {log_path_1}")
        lines_count = 1113
        utils.touch(log_path)
        utils.touch(log_path_1)
        t = _log_generator_thread(log_path, lines_count, {500: 2})
        t.start()
        log_snapshot.start(log_path_1, f"while true; do bash -c \"cat {log_path} > {log_path_1}; sleep 0.01; sync\"; done", 500)
        t.join()
        time.sleep(0.5)
        log_snapshot.stop()
        _restart_command.assert_has_calls(call())
        print("post test_log_with_timestamps_timeout")
        with open(log_path_1, "r") as f:
            rlines = f.readlines()
            self.assertEqual(lines_count, len(rlines))
            self.assertEqual(lines_count, len(_generated_lines))
            for idx in range(len(rlines)):
                self.assertEqual(rlines[idx], _generated_lines[idx])
