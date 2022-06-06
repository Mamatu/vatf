from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import errno

import logging
import textwrap
import os

from vatf.api import mkdir

class MkdirTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    def setUp(self):
        from vatf.utils import config
        logging.getLogger().setLevel(logging.INFO)
        config.reset()
    @patch("os.makedirs")
    @patch("os.listdir")
    def test_mkdir_with_counter(self, os_listdir_mock, os_makedirs_mock):
        os_listdir_mock.return_value = ["session_0"]
        mkdir.mkdir_with_counter("/tmp/session")
        self.assertTrue(os_makedirs_mock.called)
        self.assertTrue("/tmp/session_1", os_makedirs_mock.call_args)
