from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import errno

import datetime
import logging
import textwrap
import os

from vatf.utils import utils

class UtilsTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
        self.test_file = None
        self.remove_test_file = True
    def  setUp(self):
        self.test_file = utils.get_temp_filepath()
    def tearDown(self):
        if self.remove_test_file and os.path.exists(self.test_file):
            os.remove(self.test_file)
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
    def test_grep_empty(self):
        testfile_path = self.test_file
        with open(testfile_path, "w") as f:
            f.write("")
        out = utils.grep(testfile_path, "2")
        self.assertEqual([], out)
    def test_grep(self):
        testfile_path = self.test_file
        with open(testfile_path, "w") as f:
            f.write("1\n2")
        out = utils.grep(testfile_path, "2")
        self.assertTrue(len(out) == 1)
        self.assertEqual("2", out[0].matched)
    def test_grep_one_regex_repeated(self):
        testfile_path = self.test_file
        with open(testfile_path, "w") as f:
            f.write("ada\nada\nada")
        out = utils.grep(testfile_path, "ada")
        self.assertTrue(len(out) == 3)
        self.assertEqual("ada", out[0].matched)
        self.assertEqual("ada", out[1].matched)
        self.assertEqual("ada", out[2].matched)
    def test_grep_one_regex_in_bias(self):
        testfile_path = self.test_file
        with open(testfile_path, "w") as f:
            f.write("ada\ndud\nada\ndud\nada\nada")
        out = utils.grep(testfile_path, "ada")
        self.assertTrue(len(out) == 4)
        self.assertEqual("ada", out[0].matched)
        self.assertEqual(1, out[0].line_number)
        self.assertEqual("ada", out[1].matched)
        self.assertEqual(3, out[1].line_number)
        self.assertEqual("ada", out[2].matched)
        self.assertEqual(5, out[2].line_number)
        self.assertEqual("ada", out[3].matched)
        self.assertEqual(6, out[3].line_number)
    def test_grep_line_regex_with_line_number(self):
        testfile_path = self.test_file
        with open(testfile_path, "w") as f:
            f.write("2021-12-19 17:59:17.171 [ 15] I start")
            f.write("\n")
            f.write("2021-12-19 17:59:17.172 [ 15] I end")
        line_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
        out = utils.grep_regex_in_line(testfile_path, "start", line_regex)
        self.assertEqual(1, out[0].line_number)
        self.assertEqual("2021-12-19 17:59:17.171", out[0].matched[0])
        self.assertTrue(len(out) == 1)
        out = utils.grep_regex_in_line(testfile_path, "end", line_regex)
        self.assertEqual(2, out[0].line_number)
        self.assertEqual("2021-12-19 17:59:17.172", out[0].matched[0])
        self.assertTrue(len(out) == 1)
    def test_grep_line_regex_with_line_two_lines(self):
        testfile_path = self.test_file
        with open(testfile_path, "w") as f:
            f.write("2021-12-19 17:59:17.171 [ 15] I regex")
            f.write("\n")
            f.write("2021-12-19 17:59:17.172 [ 15] I regex")
        line_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
        out = utils.grep_regex_in_line(testfile_path, "regex", line_regex)
        self.assertEqual(2, len(out))
        self.assertEqual(1, out[0].line_number)
        self.assertEqual(2, out[1].line_number)
        self.assertEqual("2021-12-19 17:59:17.171", out[0].matched[0])
        self.assertEqual("2021-12-19 17:59:17.172", out[1].matched[0])
    def test_get_total_milliseconds(self):
        date1 = datetime.datetime.strptime("2021-12-19 17:59:17.171", utils.DATE_FORMAT)
        date2 = datetime.datetime.strptime("2021-12-19 17:59:18.171", utils.DATE_FORMAT)
        self.assertEqual(1000, utils.get_total_milliseconds(date2 - date1))
    def test_grep_line_regex_with_line_two_lines(self):
        testfile_path = self.test_file
        with open(testfile_path, "w") as f:
            f.write("regex")
            f.write("\n")
            f.write("2021-12-19 17:59:17.171 [ 15] I regex")
            f.write("\n")
            f.write("regex")
            f.write("\n")
            f.write("2021-12-19 17:59:17.172 [ 15] I regex")
            f.write("\n")
            f.write("regex")
        line_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
        out = utils.grep_regex_in_line(testfile_path, "regex", line_regex)
        self.assertEqual(2, len(out))
        self.assertEqual(2, out[0].line_number)
        self.assertEqual(4, out[1].line_number)
        self.assertEqual("2021-12-19 17:59:17.171", out[0].matched[0])
        self.assertEqual("2021-12-19 17:59:17.172", out[1].matched[0])
