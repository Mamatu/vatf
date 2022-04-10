from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import errno

import logging
import textwrap
import mkdir
import os

import sleep

class SleepTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    def test_sleep(self):
        sleep.SleepUntilTimeout(0.1)
