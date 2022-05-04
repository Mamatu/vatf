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
        text = [
        "2022-01-29 20:54:55.567 line1\n",
        "2022-01-29 20:54:55.567 line2\n",
        "2022-01-29 20:54:55.568 line3\n",
        "2022-01-29 20:54:55.569 line4\n",
        "2022-01-29 20:54:55.570 line5\n",
        "2022-01-29 20:54:55.600 line6\n",
        "2022-01-29 20:54:56.568 line7\n"
        ]
        with patch.object(sys, 'argv', ['', '', 'executor/tests/data/config.json']):
            path1 = self.create_file("w", text)
            path2 = utils.get_temp_filepath()
            DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
            now = datetime.datetime.strptime("2022-01-29 20:54:55.569", DATE_FORMAT)
            log_snapshot.start(log_path = path1, snapshot_path = path2, now = now)
            log_snapshot.stop()
            with open(path2, "r") as f:
                text = f.readlines()
                logging.debug(text)
                self.assertEqual(4, len(text))
                self.assertEqual(text[0].rstrip(), "2022-01-29 20:54:55.569 line4")
                self.assertEqual(text[1].rstrip(), "2022-01-29 20:54:55.570 line5")
                self.assertEqual(text[2].rstrip(), "2022-01-29 20:54:55.600 line6")
                self.assertEqual(text[3].rstrip(), "2022-01-29 20:54:56.568 line7")
            os.remove(path1)
            os.remove(path2)
    def test_log_without_timestamps(self):
        text = [
        "2022-01-29 20:54:55.567 line1\n",
        "line1\n",
        "2022-01-29 20:54:55.567 line2\n",
        "line2\n",
        "2022-01-29 20:54:55.568 line3\n",
        "line3\n",
        "2022-01-29 20:54:55.569 line4\n",
        "line4\n",
        "2022-01-29 20:54:55.570 line5\n",
        "line5\n",
        "2022-01-29 20:54:55.600 line6\n",
        "line6\n",
        "2022-01-29 20:54:56.568 line7\n"
        "line7\n",
        ]
        with patch.object(sys, 'argv', ['', '', 'executor/tests/data/config.json']):
            path1 = self.create_file("w", text)
            path2 = utils.get_temp_filepath()
            DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
            now = datetime.datetime.strptime("2022-01-29 20:54:55.569", DATE_FORMAT)
            log_snapshot.start(path1, path2, now = now)
            log_snapshot.stop()
            with open(path2, "r") as f:
                text = f.readlines()
                logging.debug(text)
                self.assertEqual(7, len(text))
                #self.assertEqual(8, len(text))
                self.assertEqual(text[0].rstrip(), "2022-01-29 20:54:55.569 line4"),
                self.assertEqual(text[1].rstrip(), "line4"),
                self.assertEqual(text[2].rstrip(), "2022-01-29 20:54:55.570 line5"),
                self.assertEqual(text[3].rstrip(), "line5")
                self.assertEqual(text[4].rstrip(), "2022-01-29 20:54:55.600 line6")
                self.assertEqual(text[5].rstrip(), "line6")
                self.assertEqual(text[6].rstrip(), "2022-01-29 20:54:56.568 line7")
                #self.assertEqual(text[7].rstrip(), "line7")
            os.remove(path1)
            os.remove(path2)
    def test_log_(self):
        with patch.object(sys, 'argv', ['', '', 'executor/tests/data/config.json']):
            path2 = utils.get_temp_filepath()
            DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
            now = datetime.datetime.strptime("2022-02-03 17:32:34.090", DATE_FORMAT)
            log_snapshot.start(log_path = "executor/tests/data/test.log", snapshot_path = path2, now = now)
            section = log_snapshot.stop()
            with open(path2, "r") as f:
                text = f.readlines()
                logging.debug(text)
                self.assertEqual(4, len(text))
