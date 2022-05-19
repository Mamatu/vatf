from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import errno
import datetime
import logging
import textwrap
import os

import sys

from vatf.executor import log_snapshot
from vatf.utils import utils, config

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
        t.start()
        log_snapshot.start()
        t.join()
        log_file.close()
