from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import errno
import datetime
import logging
import textwrap
import logger
import os

from vatf_utils import utils

class LoggerTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
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
        path1 = self.create_file("w", text)
        path2 = utils.get_temp_filepath()
        DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
        now = datetime.datetime.strptime("2022-01-29 20:54:55.569", DATE_FORMAT)
        logger.Start(now, path1, path2)
        logger.WaitForLine()
        logger.Stop()
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
        path1 = self.create_file("w", text)
        path2 = utils.get_temp_filepath()
        DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
        now = datetime.datetime.strptime("2022-01-29 20:54:55.569", DATE_FORMAT)
        logger.Start(now, path1, path2)
        logger.WaitForLine()
        logger.Stop()
        with open(path2, "r") as f:
            text = f.readlines()
            logging.debug(text)
            self.assertEqual(8, len(text))
            self.assertEqual(text[0].rstrip(), "2022-01-29 20:54:55.569 line4"),
            self.assertEqual(text[1].rstrip(), "line4"),
            self.assertEqual(text[2].rstrip(), "2022-01-29 20:54:55.570 line5"),
            self.assertEqual(text[3].rstrip(), "line5")
            self.assertEqual(text[4].rstrip(), "2022-01-29 20:54:55.600 line6")
            self.assertEqual(text[5].rstrip(), "line6")
            self.assertEqual(text[6].rstrip(), "2022-01-29 20:54:56.568 line7")
            self.assertEqual(text[7].rstrip(), "line7")
        os.remove(path1)
        os.remove(path2)
    def test_log_(self):
        path2 = utils.get_temp_filepath()
        DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
        now = datetime.datetime.strptime("2022-02-03 17:32:34.090", DATE_FORMAT)
        logger.Start(now, "tests/data/test.log", path2)
        logger.WaitForLine()
        logger.Stop()
        with open(path2, "r") as f:
            text = f.readlines()
            logging.debug(text)
            self.assertEqual(4, len(text))
