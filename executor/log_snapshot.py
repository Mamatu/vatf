"""
Takes the snapshot of log between start and stop method.
"""
import logging

import datetime
import time

from vatf.executor import shell, mkdir
from vatf.vatf_api import public_api

from vatf.utils import logger_thread
from vatf.utils import utils, os_proxy

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from threading import Timer, Lock

_ctx = None
_observer = None
_timer = None
_timepoint = None
_mutex = Lock()
_restart_timeout = None
_restart_command = None
_log_path = None
_shell_cmd = None
_shell_cmd_process = None

def _lock(func):
    def wrapper():
        global _mutex
        _mutex.acquire()
        try:
            return func()
        finally:
            _muter.release()
    return wrapper

def _setup_command(shell_cmd, shell_cmd_rtimeout, log_path):
    global _log_path, _restart_timeout, _shell_cmd
    _restart_timeout = shell_cmd_rtimeout
    _log_path = log_path
    _shell_cmd = shell_cmd

def _start_command():
    global _shell_cmd, _shell_cmd_process, _restart_command
    def restart():
        global _shell_cmd_process, _shell_cmd
        if _shell_cmd_proces: shell.kill(_shell_cmd_process)
        _shell_cmd_process = shell.bg(_shell_cmd)
    _restart_command = restart
    restart()

def _start_timer():
    #from https://stackoverflow.com/a/48741004
    class _RepeatTimer(Timer):
        def run(self):
            while not self.finished.wait(self.interval):
                self.function(*self.args, **self.kwargs)
    @_lock
    def timepoint_observer():
        global _timepoint, _restart_command, _restart_timeout
        _current_timepoint = time.time()
        if abs(_current_timepoint - _timepoint) > _restart_timeout:
            _restart_command()


def _start_observer(log_path, restart_timeout):
    global _observer, _timer
    class _MonitorHandler(FileSystemEventHandler):
        def __init__(self, log_path, on_log_modified):
            self.log_path = log_path
            self.on_log_modified = on_log_modified
        def on_modified(self, event):
            if event.is_directory: return
            src_path = event.src_path
            if src_path == self.log_path:
                self.on_log_modified()
    observer = Observer()
    @_lock
    def update_timepoint():
        global _timepoint
        _timepoint = time.time()
    monitor_handler = _MonitorHandler(_log_path, update_timepoint)
    observer.schedule(monitor_handler, path = log_path, recursive = False)
    observer.start()
    _observer = observer

@public_api("log_snapshot")
def start(log_path, shell_cmd, restart_timeout):
    if shell_cmd:
        shell_cmd = shell_cmd.format(session_path = session_path)
        _setup_command(shell_cmd, shell_cmd_rtimeout, log_path)
        _start_command()
        _start_timer()
        _start_observer(log_path, shell_cmd_rtimeout)
    else:
        raise Exception("Only variant with shell_cmd is currently supported")

@public_api("log_snapshot")
def start_from_config():
    global _ctx
    if _ctx:
        raise Exception(f"{start.__name__} Log snapshot is already started!")
    shell_cmd = config.get_shell_command()
    shell_cmd_rtimeout = config.get_shell_command_restart_timeout()
    if not ((shell_cmd != None and shell_cmd_rtimeout != None) or (shell_cmd == None and shell_cmd_rtimeout == None)):
        raise Exception("shell_cmd and shell_cmd_rtimeout must be defined or both not defined")
    session_path = mkdir.mkdir_with_counter("./logs/session")
    log_path = command.get_log_path()
    log_path = log_path.format(session_path = session_path)
    start(log_path, shell_cmd, shell_cmd_rtimeout)

def stop():
    global _ctx
    try:
        if not _ctx:
            raise Exception(f"{stop.__name__} was not called start before!")
        start_line = -1
        end_line = -1
        results = utils.grep_regex_in_line(_ctx.log_path, grep_regex = ".*", match_regex = utils.DATE_REGEX)
        logging.debug(f"{stop.__name__} founds {len(results)} results")
        for result in results:
            dt = datetime.datetime.strptime(result.matched[0], utils.DATE_FORMAT)
            logging.debug(f"{stop.__name__} founds datetime in line {dt} and compares to {_ctx.now}")
            diff = dt - _ctx.now
            logging.debug(f"{stop.__name__} {diff} > {datetime.timedelta()}")
            if diff >= datetime.timedelta():
                if start_line == -1:
                    start_line = result.line_number - 1
                    logging.debug(f"{stop.__name__} found start line {start_line}")
                if end_line == -1 or result.line_number > end_line:
                    end_line = result.line_number
                    logging.debug(f"{stop.__name__} updated end line {end_line}")
        lf_lines = None
        with os_proxy.open_to_read(_ctx.log_path) as lf:
            lf_lines = lf.readlines()
            with os_proxy.open_to_write(_ctx.snapshot_path) as sf:
                lf_lines = lf_lines[start_line : end_line]
                sf.writelines(lf_lines)
        _ctx = None
        return (start_line, end_line)
    finally:
        _ctx = None
