__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

def test_thread_with_stop():
    from vatf.utils.thread_with_stop import Thread
    def target(is_stopped):
        while not is_stopped():
            pass
    t = Thread(target = target)
    t.start()
    t.stop()
    t.join()

def test_thread_with_stop_1():
    from vatf.utils.thread_with_stop import Thread
    def target(output, is_stopped):
        while not is_stopped():
            output[0] = 2
    output = [1]
    t = Thread(target = target, args = [output])
    t.start()
    import time
    time.sleep(.1)
    t.stop()
    t.join()
    assert output[0] == 2
