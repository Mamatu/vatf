__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

"""
Takes the snapshot of log between start and stop method.
"""

from vatf.executor import shell

class LogSnapshot:
    def __init__(self):
        self._log_path = None
        self._shell_cmd = None
        self._shell_process = None
        self._thread = None
 
    def start_cmd(self, log_path, shell_cmd):
        """
        Starts log_snapshot which will use shell cmd to fill out log_path
        """
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
        import os
        if not os.path.exists(in_log_path):
            raise Exception(f"File {in_log_path} does not exist")
        from vatf.utils import config_handler
        from vatf.utils.kw_utils import handle_kwargs
        config = None
        try:
            config = config_handler.get_config(**kwargs)
        except config_handler.NoConfigException:
            pass
        timestamp_regex = None
        timestamp_format = None
        timestamp_delta = None
        if config:
            timestamp_regex = config["va_log.date_regex"]
            timestamp_format = config["va_log.date_format"]
            timestamp_delta = None
            try:
                timestamp_delta = config["va_log.timedelta"]
                from vatf.utils import config_common
                timestamp_delta = config_common.convert_dict_to_timedelta(timestamp_delta)
            except KeyError:
                pass
        else:
            timestamp_regex = handle_kwargs("timestamp_regex", is_required = True, **kwargs)
            timestamp_format = handle_kwargs("timestamp_format", is_required = True, **kwargs)
            timestamp_delta = handle_kwargs("timestamp_delta", is_required = False, **kwargs)
        pause = handle_kwargs("pause", default_output = 0.2, is_required = False, **kwargs)
        from vatf.executor import search
        from datetime import datetime
        now = datetime.now()
        if timestamp_delta:
            now = now + timestamp_delta
        outputs = search.find(timestamp_regex, filepath = in_log_path, only_match = True)
        outputs = list(map(lambda x: (datetime.strptime(x[1], timestamp_format), x), outputs))
        from vatf.utils.binary_search import binary_search
        line_number = binary_search(outputs, lambda x: x[0] < now, lambda x: now < x[0])[1].line_number
        from vatf.executor import shell
        from vatf.utils.thread_with_stop import Thread
        self._log_path = log_path
        def copy_file(line_number, in_log_path, log_path, pause, is_stopped):
            import time
            while not is_stopped():
                shell.fg(f"tail --lines=+{line_number} {in_log_path} > {log_path}")
                time.sleep(pause)
        self._thread = Thread(target = copy_file, args = [line_number, in_log_path, log_path, pause])
        self._thread.start()

    def get_lines_count(self):
        if self._log_path is None:
            raise Exception("Lack of file to line count")
        output = shell.fg(f"wc -l {self._log_path}")
        output = output.replace(self._log_path, "")
        output = output.replace(" ", "")
        return int(output)

    def remove_head(self, line_count):
        from vatf.executor import shell
        shell.fg(f"sed -i '{line_count}d' {self._log_path}")

    def stop(self):
        self._stop_command()
        self._stop_thread()

    def _stop_command(self):
        if self._shell_process:
            from vatf.executor import shell
            shell.kill(self._shell_process)
            self._shell_process = None

    def _stop_thread(self):
        if self._thread:
            self._thread.stop()
            self._thread.join()
            self._thread = None

def make():
    return LogSnapshot()
