__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from unittest import TestCase
from unittest.mock import Mock

import logging

from vatf.utils import loop
from timeit import default_timer as timer
from datetime import timedelta

def test_loop_async():
    start = timer()
    def callback():
        return False
    thread = loop.async_loop(callback, 10, None)
    thread.stop()
    end = timer()
    print(timedelta(seconds = end - start))
