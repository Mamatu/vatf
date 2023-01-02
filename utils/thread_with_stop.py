__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import threading

class Thread(threading.Thread):
    def __init__(self, target, args):
        self.stopped = False
        _args = []
        _args.extend(args)
        _args.append(self.is_stopped)
        super().__init__(group = None, target = target, args = _args)

    def stop(self):
        self.stopped = True

    def is_stopped(self):
        return self.stopped

    def run(self):
        super().run()
