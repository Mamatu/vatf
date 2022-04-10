from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import errno

import logging
import textwrap
import mkdir
import os

class MkdirTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    @patch("os.makedirs")
    @patch("os.listdir")
    def test_mkdir_by_counter(self, os_listdir_mock, os_makedirs_mock):
        os_listdir_mock.return_value = ["session_0"]
        mkdir.MkdirByCounter("/tmp/session")
        self.assertTrue(os_makedirs_mock.called)
        self.assertTrue("/tmp/session_1", os_makedirs_mock.call_args)
