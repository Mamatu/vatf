from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import errno

import logging
import textwrap
import os

from vatf.executor import wait

class WaitTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
