__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

"""
Takes the snapshot of log between start and stop method.
"""

from vatf.executor import shell, search
from vatf.utils.kw_utils import handle_kwargs
from vatf.utils.binary_search import binary_search
from threading import Lock

class LogSnapshot:
    class LogPathNone(Exception):
        def __init__(self):
            super().__init__("log path is none")
    def __init__(self):
        self._log_path = None
        self._shell_cmd = None
        self._shell_process = None
        self._thread = None
        self._rb_thread = None
        self._timestamp_regex = None
        self._timestamp_format = None
        self._rb_count = 0
        self._head_offset = 0
        self._lock = Lock()
    def call_safe(self, callback):
        with self._lock:
            return callback()
    def start_cmd(self, log_path, shell_cmd, **kwargs):
        """
        Starts log_snapshot which will use shell cmd to fill out log_path
        """
        now = self._handle_config_on_startup(**kwargs)
        self._log_path = log_path
        self._shell_cmd = shell_cmd
        def restart():
            from vatf.executor import shell
            if self._shell_process:
                try:
                    shell.kill(self._shell_process)
                except psutil.NoSuchProcess as nsp:
                    logging.warn(f"WARNING! {str(nsp)}")
            self._shell_process = shell.bg(self._shell_cmd)
        restart()
    def start_copy(self, log_path, in_log_path, **kwargs):
        """
        Starts log_snapshot which will copy part of in_log_path into log_path
        """
        now = self._handle_config_on_startup(**kwargs)
        import os
        if not os.path.exists(in_log_path):
            raise Exception(f"File {in_log_path} does not exist")
        pause = handle_kwargs("pause", default_output = 0.2, is_required = False, **kwargs)
        outputs = search.find(self._timestamp_regex, filepath = in_log_path, only_match = True)
        from datetime import datetime
        outputs = list(map(lambda x: (datetime.strptime(x[1], self._timestamp_format), x), outputs))
        line_number = binary_search(outputs, lambda x: x[0] < now, lambda x: now < x[0])[1].line_number
        from vatf.utils.thread_with_stop import Thread
        self._log_path = log_path
        def copy_file(self, line_number, in_log_path, log_path, pause, is_stopped):
            import time
            while not is_stopped():
                head_offset = self.call_safe(lambda: self._head_offset)
                shell.fg(f"tail --lines=+{line_number + head_offset} {in_log_path} > {log_path}")
                time.sleep(pause)
        self._thread = Thread(target = copy_file, args = [self, line_number, in_log_path, log_path, pause])
        self._thread.start()
    def get_lines_count(self):
        if self._log_path is None:
            raise LogSnapshot.LogPathNone()
        output = shell.fg(f"wc -l {self._log_path}")
        output = output.replace(self._log_path, "")
        output = output.replace(" ", "")
        return int(output)
    def get_seconds(self):
        from datetime import datetime
        first_line_timestamp = self.get_the_first_line_timestamp()
        last_line_timestamp = self.get_the_last_line_timestamp()
        if not first_line_timestamp or not last_line_timestamp:
            return 0
        ftp = datetime.strptime(first_line_timestamp, self._timestamp_format)
        ltp = datetime.strptime(last_line_timestamp, self._timestamp_format)
        d = ltp - ftp
        return d.total_seconds()
    def set_timestamp_regex(self, timestamp_regex):
        self._timestamp_regex = timestamp_regex
    def set_timestamp_format(self, timestamp_format):
        self._timestamp_format = timestamp_format
    def get_the_first_line(self):
        if self._log_path is None:
            raise LogSnapshot.LogPathNone()
        return shell.fg(f"head -n1 {self._log_path}")
    def get_the_last_line(self):
        if self._log_path is None:
            raise LogSnapshot.LogPathNone()
        return shell.fg(f"tail -n1 {self._log_path}")
    def _get_line_timestamp(self, line):
        from vatf.utils import grep
        outputs = grep.grep_in_text(line, self._timestamp_regex, only_match = True)
        if len(outputs) == 0:
            return None
        return outputs[0].matched
    def get_the_first_line_timestamp(self):
        return self._get_line_timestamp(self.get_the_first_line())
    def get_the_last_line_timestamp(self):
        return self._get_line_timestamp(self.get_the_last_line())
    def remove_head(self, lines_count):
        """
        Removes lines_count from head of log_snapshot file
        """
        if self._log_path is None:
            raise LogSnapshot.LogPathNone()
        shell.fg(f"sed -i '{lines_count}d' {self._log_path}")
    def _cutter_for_seconds(self, time_in_seconds, is_stopped):
        while not is_stopped():
            seconds = self.get_seconds()
            fl_ts = self.get_the_first_line_timestamp()
            if seconds is None or fl_ts is None:
                continue
            diff = time_in_seconds - seconds
            if diff > 0:
                outputs = search.find(self._timestamp_regex, filepath = self._log_path, only_match = True)
                outputs = list(map(lambda x: (datetime.strptime(x[1], self._timestamp_format), x), outputs))
                line_number = binary_search(outputs, lambda x: x[0] < now, lambda x: now < x[0])[1].line_number
                self.remove_head(line_number)
                self._rb_count = self._rb_count + 1
                breakpoint()
                def _call_safe():
                    self._head_offset = self._head_offset + line_number
                self.call_safe(_call_safe)
    def set_ring_buffer(self, **kwargs):
        """
        Log snapshot will work as ring buffer limited to lines_count lines
        """
        length_in_seconds = handle_kwargs("length_in_seconds", is_required = False, **kwargs)
        if not length_in_seconds:
            raise Exception("At least one param is expected: length_in_lines_count or length_in_seconds")
        from vatf.utils.thread_with_stop import Thread
        assert self._rb_thread is None, "self._rb_thread must be None"
        if length_in_seconds:
            from datetime import datetime
            self._rb_thread = Thread(target = self._cutter_for_seconds, args = [length_in_seconds])
        else:
            raise Exception("Not supported state")
        self._rb_thread.start()
    def stop(self, stop_ring_buffer_thread = True):
        self._stop_command()
        self._stop_thread(stop_ring_buffer_thread = stop_ring_buffer_thread)
    def stop_ring_buffer_thread(self):
        self.stop(stop_ring_buffer_thread = True)
    def get_ring_buffer_count(self):
        """
        Returns how many times ring buffer algorithm has worked on the file
        """
        return self._rb_count
    def _handle_config_on_startup(self, **kwargs):
        from vatf.utils import config_handler
        config = None
        try:
            config = config_handler.get_config(**kwargs)
        except config_handler.NoConfigException:
            pass
        timestamp_regex = None
        timestamp_format = None
        timestamp_delta = None
        if config:
            timestamp_regex = config["log_snapshot.date_regex"]
            timestamp_format = config["log_snapshot.date_format"]
            timestamp_delta = None
            try:
                timestamp_delta = config["log_snapshot.timedelta"]
                from vatf.utils import config_common
                timestamp_delta = config_common.convert_dict_to_timedelta(timestamp_delta)
            except KeyError:
                pass
        else:
            timestamp_regex = handle_kwargs("timestamp_regex", is_required = True, **kwargs)
            timestamp_format = handle_kwargs("timestamp_format", is_required = True, **kwargs)
            timestamp_delta = handle_kwargs("timestamp_delta", is_required = False, **kwargs)
        self.set_timestamp_format(timestamp_format)
        self.set_timestamp_regex(timestamp_regex)
        from datetime import datetime
        now = datetime.now()
        if timestamp_delta:
            now = now + timestamp_delta
        return now
    def _stop_command(self):
        if self._shell_process:
            from vatf.executor import shell
            shell.kill(self._shell_process)
            self._shell_process = None
    def _stop_thread(self, stop_ring_buffer_thread = True):
        if self._thread:
            self._thread.stop()
            self._thread.join()
            self._thread = None
        if self._rb_thread and stop_ring_buffer_thread:
            self._rb_thread.stop()
            self._rb_thread.join()
            self._rb_thread = None

def make():
    return LogSnapshot()
