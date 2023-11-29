__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from unittest import TestCase
from unittest.mock import MagicMock

import logging

from vatf.utils import loop
from timeit import default_timer as timer
from datetime import timedelta

import threading
import time

def test_loop_async_callback_stop():
    start = timer()
    callback = MagicMock()
    def side_effect(pause_thread_control):
        return True
    callback.side_effect = side_effect
    thread = loop.async_loop(callback, 0.01, None)
    end = timer()
    td = timedelta(seconds = end - start)
    assert td < timedelta(microseconds = 10000)
    callback.assert_called_once()

def test_loop_async_thread_stop():
    start = timer()
    callback = MagicMock()
    lock = threading.Lock()
    def side_effect(pause_thread_control):
        return False
    callback.side_effect = side_effect
    thread = loop.async_loop(callback, 0.01, None)
    assert loop.wait_until_true(lambda: callback.called, 0.01, 5)
    thread.stop()
    end = timer()
    td = timedelta(seconds = end - start)
    assert td < timedelta(microseconds = 10000)
    callback.assert_called()

def test_loop_async_thread_pause_resume():
    start = timer()
    callback = MagicMock()
    lock = threading.Lock()
    pause = None
    def side_effect(pause_thread_control):
        nonlocal pause, lock
        with lock:
            if pause is not None:
                pause()
                return True
        return False
    callback.side_effect = side_effect
    thread = loop.async_loop(callback, 0.01, None)
    assert loop.wait_until_true(lambda: callback.called, 0.001, 5)
    with lock:
        pause = thread.pause
    assert loop.wait_until_true(thread.is_paused, 0.001, 5)
    thread.resume()
    end = timer()
    td = timedelta(seconds = end - start)
    print(td)
    #assert td < timedelta(microseconds = 100000)
    assert td < timedelta(microseconds = 50000)
    callback.assert_called()
