__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import errno

import datetime
import logging
import textwrap
import os

from vatf.utils import utils

TIMESTAMP_REGEX = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

class TestUtils(TestCase):
    def setup_method(self, method):
        self.test_file = utils.get_temp_file()
    def teardown_method(self, method):
        self.test_file.close()
    @patch("os.listdir")
    def test_find_in_dir_no_matches(self, os_listdir_mock):
        os_listdir_mock.return_value = ["s_1", "r"]
        found = utils.find_in_dir("/tmp/", "session")
        self.assertEqual([], found)
    @patch("os.listdir")
    def test_find_in_dir(self, os_listdir_mock):
        os_listdir_mock.return_value = ["session_1", "session_2", "s_1", "r"]
        found = utils.find_in_dir("/tmp/", "session")
        self.assertEqual(["session_1", "session_2"], found)
    @patch("os.listdir")
    def test_find_in_dir_exception(self, os_listdir_mock):
        os_listdir_mock.side_effect = FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "")
        found = utils.find_in_dir("/tmp1/", "session")
        self.assertEqual([], found)
    def test_parse_number(self):
        self.assertEqual(-1, utils.parse_number_suffix("session"))
        self.assertEqual(-1, utils.parse_number_suffix("session_"))
        self.assertEqual(0, utils.parse_number_suffix("session_0"))
        self.assertEqual(1, utils.parse_number_suffix("session_1"))
        self.assertEqual(10, utils.parse_number_suffix("session_10"))
        self.assertEqual(101, utils.parse_number_suffix("session_101"))
        self.assertEqual(1012, utils.parse_number_suffix("session_1012"))
        self.assertEqual(1012, utils.parse_number_suffix("ses1sion_1012"))
    @patch("os.listdir")
    def test_get_counter(self, os_listdir_mock):
        os_listdir_mock.return_value = ["session_1", "session_2", "s_1", "r"]
        self.assertEqual(2, utils.get_counter("/tmp/", "session"))
    @patch("os.listdir")
    def test_get_counter_wav(self, os_listdir_mock):
        os_listdir_mock.return_value = ["sample_1.wav", "sample_2.wav", "s_1", "r"]
        self.assertEqual(2, utils.get_counter("/tmp/", "sample_", "wav"))
    @patch("os.listdir")
    def test_get_counter_exception(self, os_listdir_mock):
        os_listdir_mock.side_effect = FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "")
        self.assertEqual(-1, utils.get_counter("/tmp1/", "session"))
    def test_get_total_milliseconds(self):
        date1 = datetime.datetime.strptime("2021-12-19 17:59:17.171", TIMESTAMP_FORMAT)
        date2 = datetime.datetime.strptime("2021-12-19 17:59:18.171", TIMESTAMP_FORMAT)
        self.assertEqual(1000, utils.get_total_milliseconds(date2 - date1))
