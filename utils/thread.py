__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import threading

_lock_debug_mode = False

def lock(mutex, debug_mode = None):
    def wrap(func):
        def wrapper(*args, **kwargs):
            nonlocal mutex
            with mutex:
                return func(*args, **kwargs)
        return wrapper
    return wrap

class _RepeatTimer(threading.Timer):
    def run(self):
        while not self.finished.is_set():
            self.finished.wait(self.interval)
            if not self.finished.is_set():
                self.function(*self.args, **self.kwargs)
        self.finished.set()

def make_repeat_timer(function, interval, *args, **kwargs):
    return _RepeatTimer(function = function, interval = interval, *args, **kwargs)

def enable_lock_debug_mode(enable = True):
    global _lock_debug_mode
    _lock_debug_mode = enable
    return _lock_debug_mode

def get_lock_debug_mode():
    global _lock_debug_mode
    return _lock_debug_mode

def is_debug(debug_mode):
    global _lock_debug_mode
    if debug_mode == None:
        return _lock_debug_mode
    else:
        return debug_mode

def _lock(mutex, func, debug_mode):
    if is_debug(debug_mode):
        print(f"pre_lock {func.__name__}")
    mutex.acquire()
    if is_debug(debug_mode):
        print(f"post_lock {func.__name__}")

def _unlock(mutex, func, debug_mode):
    if is_debug(debug_mode):
        print(f"pre_unlock {func.__name__}")
    mutex.acquire()
    if is_debug(debug_mode):
        print(f"post_unlock {func.__name__}")

