__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import threading

class Thread(threading.Thread):
    def __init__(self, target, args = [], kwargs = {}):
        self.stopped = False
        self.args = args
        self.kwargs = kwargs
        self.mutex = threading.RLock()
        self.target = target
        super().__init__()

    def stop(self):
        try:
            self.mutex.acquire()
            self.stopped = True
        finally:
            self.mutex.release()

    def is_stopped(self):
        try:
            self.mutex.acquire()
            return self.stopped
        finally:
            self.mutex.release()

    def run(self):
        return self.target(*self.args, is_stopped = lambda: self.is_stopped(), **self.kwargs)
