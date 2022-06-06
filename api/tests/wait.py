from unittest import TestCase
from unittest.mock import Mock, MagicMock
from unittest.mock import patch, call, ANY

import errno

import logging
import textwrap
import os

from vatf.api import wait
from vatf.utils import os_proxy, utils

import datetime
import threading
import time
import tracemalloc

tracemalloc.start()
class WaitTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    def setUp(self):
        from vatf.utils import config
        logging.getLogger().setLevel(logging.INFO)
        config.reset()
    def create_file(self, mode, data = None):
        path = utils.get_temp_filepath()
        with open(path, mode) as f:
            if data:
                if isinstance(data, str):
                    f.write(data)
                if isinstance(data, list):
                    f.writelines(data)
        return path
    @patch("vatf.utils.config.convert_to_log_zone")
    def test_wait_for_regex(self, convert_to_log_zone):
        convert_to_log_zone.side_effect = lambda dt: dt #ToDo: To overload config loading, it should be removed in the future
        callbacks = wait.WfrCallbacks()
        callbacks.success = MagicMock()
        callbacks.timeout = MagicMock()
        callbacks.pre_sleep = MagicMock()
        text = [
        "2022-01-29 20:54:55.567 line1\n",
        "2022-01-29 20:54:55.567 line2\n",
        "2022-01-29 20:54:55.568 line3\n",
        "2022-01-29 20:54:55.569 line4\n",
        "2022-01-29 20:54:55.570 line5\n",
        "2022-01-29 20:54:55.600 line6\n",
        "2022-01-29 20:54:56.568 line7\n"
        ]
        log_path = os_proxy.create_file("w", data = "".join(text))
        start_time = datetime.datetime.strptime("2022-01-29 20:54:55.567", utils.TIMESTAMP_FORMAT)
        wait.wait_for_regex("line7", log_path, callbacks = callbacks)
        line7_timestamp = datetime.datetime.strptime("2022-01-29 20:54:56.568", utils.TIMESTAMP_FORMAT)
        callbacks.success.assert_has_calls([call(7, "line7")])
        self.assertFalse(callbacks.timeout.called)
        self.assertFalse(callbacks.pre_sleep.called)
    @patch("vatf.utils.config.convert_to_log_zone")
    def test_wait_for_regex_timeout(self, convert_to_log_zone):
        convert_to_log_zone.side_effect = lambda dt: dt #ToDo: To overload config loading, it should be removed in the future
        callbacks = wait.WfrCallbacks()
        callbacks.success = MagicMock()
        callbacks.timeout = MagicMock()
        callbacks.pre_sleep = MagicMock()
        text = [
        "2022-01-29 20:54:55.567 line1\n",
        "2022-01-29 20:54:55.567 line2\n",
        "2022-01-29 20:54:55.568 line3\n",
        "2022-01-29 20:54:55.569 line4\n",
        "2022-01-29 20:54:55.570 line5\n",
        "2022-01-29 20:54:55.600 line6\n",
        ]
        log_path = os_proxy.create_file("w", data = "".join(text))
        # ToDo: in this test in wait_for_regex should be used mocked timer.sleep not real!
        start_time = datetime.datetime.strptime("2022-01-29 20:54:55.567", utils.TIMESTAMP_FORMAT)
        timeout = datetime.timedelta(seconds = 0.5)
        pause = datetime.timedelta(seconds = 0.5)
        pause1 = datetime.timedelta(seconds = 0.45)
        pause2 = datetime.timedelta(seconds = 0.51)
        wait.wait_for_regex("line7", log_path, callbacks = callbacks, timeout = timeout, pause = pause)
        callbacks.timeout.assert_has_calls([call(timeout)])
        self.assertFalse(callbacks.success.called)
        c_args = callbacks.pre_sleep.call_args
        c_args = c_args[0]
        if isinstance(c_args, tuple): # ToDo: workaround for python 3.6 and 3.7 which in different way handle call_args
            c_args = c_args[0]
        self.assertTrue(isinstance(c_args, datetime.timedelta), f"{c_args}")
        fail_msg = f"Condition doesn't pass: {pause1} < {c_args} and {c_args} < {pause2}"
        self.assertTrue(pause1 < c_args and c_args < pause2, fail_msg)
    @patch("vatf.utils.config.convert_to_log_zone")
    def test_wait_for_regex_monitor(self, convert_to_log_zone):
        log_path = utils.get_temp_filepath()
        log_file = open(log_path, "a")
        utils.touch(log_path)
        def log_generator():
            nonlocal log_file
            counter = 0
            while counter <= 40:
                log_line = f"line{counter + 1}"
                now = datetime.datetime.now()
                line = f"{now} {log_line}\n"
                log_file.write(line)
                log_file.flush()
                logging.debug(f"Write {line} into {log_path}")
                time.sleep(0.1)
                counter = counter + 1
        t = threading.Thread(target = log_generator)
        convert_to_log_zone.side_effect = lambda dt: dt #ToDo: To overload config loading, it should be removed in the future
        callbacks = wait.WfrCallbacks()
        callbacks.success = MagicMock()
        callbacks.timeout = MagicMock()
        callbacks.pre_sleep = MagicMock()
        t.start()
        wait.wait_for_regex("line20", log_path, callbacks = callbacks, timeout = 20, pause = 0.5)
        wait.wait_for_regex("line39", log_path, callbacks = callbacks, timeout = 20, pause = 0.5)
        t.join()
        log_file.close()
