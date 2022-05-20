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
from vatf.utils.utils import lock

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from threading import Timer, RLock

@public_api("log_snapshot")
def start(log_path, shell_cmd, restart_timeout):
    if shell_cmd:
        _setup_command(shell_cmd, restart_timeout, log_path)
        _start_command()
        _start_timer()
        _start_observer(log_path, restart_timeout)
    else:
        raise Exception("Only variant with shell_cmd is currently supported")

@public_api("log_snapshot")
def start_from_config():
    global _ctx
    if _ctx:
        raise Exception(f"{start.__name__} Log snapshot is already started!")
    shell_cmd = config.get_shell_command()
    restart_timeout = config.get_shell_command_restart_timeout()
    if not ((shell_cmd != None and restart_timeout != None) or (shell_cmd == None and restart_timeout == None)):
        raise Exception("shell_cmd and restart_timeout must be defined or both not defined")
    session_path = mkdir.mkdir_with_counter("./logs/session")
    log_path = command.get_log_path()
    log_path = log_path.format(session_path = session_path)
    shell_cmd = shell_cmd.format(session_path = session_path)
    start(log_path, shell_cmd, restart_timeout)

_ctx = None
_observer = None
_timer = None
_timepoint = None
_mutex = RLock()
_restart_timeout = None
_restart_command = None
_log_path = None
_shell_cmd = None
_shell_cmd_process = None

def _setup_command(shell_cmd, restart_timeout, log_path):
    global _log_path, _restart_timeout, _shell_cmd
    _restart_timeout = restart_timeout
    _log_path = log_path
    _shell_cmd = shell_cmd

def _start_command():
    global _shell_cmd, _shell_cmd_process, _restart_command
    @lock(_mutex)
    def restart():
        global _shell_cmd_process, _shell_cmd
        if _shell_cmd_process: shell.kill(_shell_cmd_process)
        _shell_cmd_process = shell.bg(_shell_cmd)
    _restart_command = restart
    restart()

def _stop_command():
    global _shell_cmd_process
    if _shell_cmd_process:
        shell.kill(_shell_cmd_process)
        _shell_cmd_process = None

def _start_timer():
    #from https://stackoverflow.com/a/48741004
    class _RepeatTimer(Timer):
        def run(self):
            while not self.finished.wait(self.interval):
                self.function(*self.args, **self.kwargs)
    @lock(_mutex)
    def timepoint_observer():
        global _timepoint, _restart_command, _restart_timeout
        _current_timepoint = time.time()
        if _timepoint and abs(_current_timepoint - _timepoint) * 1000 > _restart_timeout:
            _restart_command()
        _timepoint = _current_timepoint

def _start_observer(log_path, restart_timeout):
    global _observer, _timer
    class _MonitorHandler(FileSystemEventHandler):
        def __init__(self, log_path, on_log_modified):
            self.log_path = log_path
            self.on_log_modified = on_log_modified
        def on_modified(self, event):
            if event.is_directory: return
            if event.src_path == self.log_path:
                #if self.on_log_modified == None: import pdb; pdb.set_trace()
                self.on_log_modified()
    observer = Observer()
    @lock(_mutex)
    def update_timepoint():
        global _timepoint
        _timepoint = time.time()
    monitor_handler = _MonitorHandler(_log_path, update_timepoint)
    _observer = observer
    observer.schedule(monitor_handler, path = log_path, recursive = False)
    observer.start()

@lock(_mutex)
def _stop_observer():
    global _observer
    if _observer:
        _observer.stop()
        _observer.join()
        _observer = None

@lock(_mutex)
def stop():
    _stop_observer()
    _stop_command()

import atexit
atexit.register(stop)
