__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from unittest import TestCase
from unittest.mock import Mock, call
from unittest.mock import patch

import errno

import datetime
import logging
import textwrap
import os

from vatf.utils.thread import make_repeat_timer

class ThreadTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
        self.test_file = None
        self.remove_test_file = True
    def  setUp(self):
        pass
    def tearDown(self):
        pass
    def test_repeat_thread(self):
        timer = None
        counter = 0
        callback_mock = Mock()
        def callback():
            nonlocal counter, timer
            counter = counter + 1
            if counter == 2:
                timer.cancel()
        callback_mock.side_effect = callback
        timer = make_repeat_timer(function = callback_mock, interval = 0.05)
        timer.start()
        timer.join()
        self.assertEqual(2, callback_mock.call_count)
