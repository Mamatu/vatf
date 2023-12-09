from vatf.executor import shell
from vatf.utils import thread_with_stop

import os

class DltWriter:
    def __init__(self, dlt_project_path):
        self._dlt_rootfs = os.path.join(dlt_project_path, "rootfs")
        self._dlt_example_user_path = os.path.join(self._dlt_rootfs, "bin/dlt-example-user")
        self.thread = None
    def _write(self, payload, log_level = 2, count = 1):
        return f"LD_LIBRARY_PATH={self._dlt_rootfs}/lib {self._dlt_example_user_path} -l {log_level} -n {count} -d 10 \"{payload}\""
    def write(self, payload, log_level = 2, count = 1):
        shell.fg(self._write(payload = payload, log_level = log_level, count = count))
    def write_in_async_loop(self, pre_callback):
        def _worker(pre_callback, is_stopped):
            while not is_stopped():
                payload, log_level, count = pre_callback()
                try:
                    print(f"payload {payload}")
                    shell.fg(self._write(payload = payload, log_level = log_level, count = count))
                except shell.StderrException as ex:
                    import logging
                    logging.info(f"Expected StdErrException: {ex}")
        self.thread = thread_with_stop.Thread(target = _worker, args = [pre_callback])
        self.thread.start()
    def stop(self):
        if self.thread is not None:
            self.thread.stop()
    def __del__(self):
        self.stop()

class DltDaemon:
    def __init__(self, dlt_project_path):
        self._dlt_rootfs = os.path.join(dlt_project_path, "rootfs")
        self._dlt_daemon_path = os.path.join(self._dlt_rootfs, "bin/dlt-daemon")
        self._dlt_daemon = None
    def start(self):
        self._dlt_daemon = shell.bg(self._dlt_daemon_path, shell = False)
    def stop(self):
        shell.kill(self._dlt_daemon)
