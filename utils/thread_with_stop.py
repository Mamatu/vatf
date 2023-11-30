__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import threading

class Thread(threading.Thread):
    def __init__(self, target, args = [], kwargs = {}):
        assert isinstance(args, list), "args must be list for this object"
        self.stopped = False
        self.mutex = threading.RLock()
        args.append(lambda: self.is_stopped())
        super().__init__(target = target, args = args, kwargs = kwargs)

    def stop(self):
        with self.mutex:
            self.stopped = True

    def is_stopped(self):
        with self.mutex:
            return self.stopped
