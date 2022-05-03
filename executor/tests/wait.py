from unittest import TestCase
from unittest.mock import Mock, MagicMock
from unittest.mock import patch, call, ANY

import errno

import logging
import textwrap
import os

from vatf.executor import wait
from vatf.utils import os_proxy, utils

import datetime

class WaitTests(TestCase):
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
        wait.wait_for_regex("line7", log_path, start_time = start_time, callbacks = callbacks)
        line7_timestamp = datetime.datetime.strptime("2022-01-29 20:54:56.568", utils.TIMESTAMP_FORMAT)
        callbacks.success.assert_has_calls([call(line7_timestamp, "line7")])
        self.assertFalse(callbacks.timeout.called)
        self.assertFalse(callbacks.pre_sleep.called)
