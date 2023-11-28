import time
import threading

def _check_timeout(timeout):
    return timeout is not None and timeout > 0

def wait_until_true(callback, pause, timeout):
    if _check_timeout(timeout):
        start_point = time.time()
    while True:
        status = callback()
        if status: return True
        time.sleep(pause)
        if _check_timeout(timeout):
            end_point = time.time()
            if (end_point - start_point) > timeout:
                return False

def async_loop(callback, pause_duration, timeout):
    from vatf.utils.thread_with_stop import Thread
    class PauseThread(Thread):
        def __init__(self):
            self.pause_cond = threading.Condition()
            self.break_cond = threading.Condition()
            self.paused = False
            self.pause_mutex = threading.Lock()
            def target(*args, **kwargs):
                is_stopped = args[-1]
                while not is_stopped():
                    class Control:
                        def __init__(self, pause_thread):
                            self.pause_thread = pause_thread
                        def is_paused(self):
                            return self.pause_thread.is_paused()
                        def is_stopped(self):
                            return self.pause_thread.is_stopped()
                        def wait_in_pause(self):
                            return self.pause_thread.wait_in_pause()
                    status = callback(pause_thread_control = Control(self))
                    if status: return True
                    self.wait_in_pause()
                    with self.break_cond:
                        self.break_cond.wait_for(lambda: not self.is_stopped(), pause_duration)
            #super().__init__(target, args, kwargs)
            super().__init__(target)
        def pause(self):
            with self.pause_cond:
                self.paused = True
        def resume(self):
            with self.pause_cond:
                self.paused = False
            self.pause_cond.notify()
        def is_paused(self):
            with self.pause_cond:
                return self.paused
        def wait_in_pause(self):
            self.pause_cond.wait_for(lambda: not self.is_paused(), None)
        def stop(self):
            with self.break_cond:
                super().stop()
                self.break_cond.notify()
    return PauseThread()
