__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

"""
Takes the snapshot of log between start and stop method.
"""
from vatf import vatf_api
import logging

import datetime
import time

from vatf.executor import shell, mkdir

from vatf.utils import logger_thread
from vatf.utils import utils, os_proxy
from vatf.utils.thread import lock, make_repeat_timer, enable_lock_debug_mode

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from threading import Timer, RLock

from vatf.utils import debug

class LogSnapshot:
    def __init__(self):
        self._ctx = None
        self._observer = None
        self._timer = None
        self._timepoint = None
        self._mutex = RLock()
        self._timepoint_mutex = RLock()
        self._restart_timeout = None
        self._restart_command = None
        self._repeat_timer = None
        self._log_path = None
        self._shell_cmd = None
        self._shell_cmd_process = None
 
    def start(self, log_path, shell_cmd, monitorFileLines = True):
        print(f"shell_cmd {shell_cmd}")
        if shell_cmd:
            self._setup_command(shell_cmd, None, log_path)
            self._start_command()
            self._start_timer()
        else:
            raise Exception("Only variant with shell_cmd is currently supported")

    def stop(self):
        self._stop_observer()
        self._stop_command()
        self._stop_timer()

    def _setup_command(self, shell_cmd, restart_timeout, log_path):
        self._restart_timeout = restart_timeout
        self._log_path = log_path
        self._shell_cmd = shell_cmd

    def _start_command(self):
        with self._timepoint_mutex:
            def restart():
                if self._shell_cmd_process:
                    try:
                        shell.kill(self._shell_cmd_process)
                    except psutil.NoSuchProcess as nsp:
                        logging.warn(f"WARNING! {str(nsp)}")
                self._shell_cmd_process = shell.bg(self._shell_cmd)
            _restart_command = restart
            restart()

    def _stop_command(self):
        if self._shell_cmd_process:
            shell.kill(self._shell_cmd_process)
            self._shell_cmd_process = None

    def _start_timer(self):
        if self._restart_timeout:
            #from https://stackoverflow.com/a/48741004
            @lock(self._timepoint_mutex)
            def timepoint_observer():
                self._current_timepoint = time.time()
                if self._timepoint:
                    elapsed_time = abs(self._current_timepoint - self._timepoint) * 1000
                if self._timepoint and elapsed_time > self._restart_timeout:
                    self._restart_command()
                    self._timepoint = self._current_timepoint
            self._repeat_timer = make_repeat_timer(function = timepoint_observer, interval = float(self._restart_timeout) / 4000)
            self._repeat_timer.start()

    def _remove_restart_command(self):
        with self._timepoint_mutex:
            self._restart_command = None

    def _stop_timer(self):
        if self._repeat_timer:
            self._repeat_timer.cancel()

    def _start_observer(self, log_path, restart_timeout):
        class _MonitorHandler(FileSystemEventHandler):
            def __init__(self, log_path, on_log_modified):
                FileSystemEventHandler.__init__(self)
                self.log_path = log_path
                self.on_log_modified = on_log_modified
            def on_modified(self, event):
                if event.is_directory: return
                if event.src_path == self.log_path:
                    self.on_log_modified()
        observer = Observer()
        @lock(self._timepoint_mutex)
        def update_timepoint():
            self._timepoint = time.time()
        if not os_proxy.exists(self._log_path):
            utils.touch(self._log_path)
        monitor_handler = _MonitorHandler(self._log_path, update_timepoint)
        self._observer = observer
        observer.schedule(monitor_handler, path = log_path, recursive = False)
        observer.start()

    def _stop_observer(self):
        if self._observer:
            self._remove_restart_command()
            self._observer.stop()
            self._observer.join()
            self._observer = None

def make():
    return LogSnapshot()
