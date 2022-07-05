from vatf import vatf_api
import time as t
import logging
from random import random
from random import randint

from vatf.utils import utils, os_proxy, config_loader

import datetime

@vatf_api.public_api("wait")
def sleep(duration):
    t.sleep(duration)

@vatf_api.public_api("wait")
def sleep_random(t1, t2):
    t.sleep(randint(t1, t2))

class WfrCallbacks:
    def __init__(self):
        pass
    def success(timestamp, matched):
        pass
    def timeout(timeout):
        pass
    def pre_sleep(time):
        pass

_log_path_set = set()
_disabled_observers = set()
_logs_lines_number = {}
_logs_observers = {}
_logs_last_line_date = {}

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import threading
_watchdog_lock = threading.RLock()

class MonitorHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory: return
        src_path = event.src_path
        if not src_path in _disabled_observers:
            logging.debug(f"modified {event} {src_path}")
            try:
                if os_proxy.exists(event.src_path): _update_line_number(src_path, 1)
            except FileNotFoundError:
                logging.warning(f"File {src_path} does not exists anymore")

def lock(func):
    def wrapper(*args):
        global _watchdog_lock
        _watchdog_lock.acquire()
        try:
            return func(*args)
        finally:
            _watchdog_lock.release()
    return wrapper

@lock
def _reset_logs_lines_number():
    global _logs_lines_number
    _logs_lines_number = {}

@lock
def _update_line_number(path, offset):
    global _logs_lines_number
    lines_number = _logs_lines_number.get(path, 1)
    _logs_lines_number[path] = lines_number + offset

@lock
def _set_line_number(path, lines_number):
    global _logs_lines_number
    _logs_lines_number[path] = lines_number

@lock
def _create_monitor(path):
    observer = Observer()
    monitor_handler = MonitorHandler()
    observer.schedule(monitor_handler, path = path, recursive = False)
    _logs_observers[path] = observer
    return observer

@lock
def _check_if_observer_added(path):
    global _logs_observers
    return path in _logs_observers

@lock
def _start_monitor(path):
    observer = None
    global _logs_observers
    try:
        observer = _logs_observers[path]
    except KeyError:
        observer = _create_monitor(path)
    observer.start()
    return observer

@lock
def _stop_monitor(path):
    observer = None
    global _logs_observers
    try:
        observer = _logs_observers[path]
    except KeyError:
        observer = _create_monitor(path)
    observer.stop()
    return observer

@lock
def _stop_all_monitors():
    global _log_path_set
    for log_path in _log_path_set:
        _stop_monitor(log_path)

import atexit
atexit.register(_stop_all_monitors)

@lock
def _pause_monitor(path):
    if not _check_if_observer_added(path):
        _start_monitor(path)
    global _disabled_observers
    _disabled_observers.add(path)

@lock
def _resume_monitor(path):
    if not _check_if_observer_added(path):
        _start_monitor(path)
    global _disabled_observers
    _disabled_observers.remove(path)

@lock
def _get_last_monitored_line(path):
    global _logs_lines_number
    return _logs_lines_number.get(path, 1)

def wait_for_regex(regex, log_path, timeout = 10, pause = 0.5, callbacks = None):
    def convert_to_timedelta(t):
        if not isinstance(t, datetime.timedelta):
            return datetime.timedelta(seconds = t)
        return t
    def call(callbacks, method_name, *args):
        if callbacks:
            method = getattr(callbacks, method_name)
            method(*args)
    def get_log_path(log_path):
        if log_path == None:
            return config.get_log_path()
        return log_path
    def _sleep(time):
        logging.debug(f"{wait_for_regex.__name__}: sleep {time}")
        call(callbacks, "pre_sleep", time)
        if isinstance(time, datetime.timedelta):
            time = time / datetime.timedelta(seconds = 1)
        t.sleep(time)
    def _init_log_path():
        nonlocal log_path
        log_path = get_log_path(log_path)
        if not os_proxy.exists(log_path): raise FileNotFoundError(log_path)
        global _log_path_set
        _log_path_set.add(log_path)
    def _wait_for_regex():
        nonlocal pause, timeout, log_path
        pause = convert_to_timedelta(pause)
        timeout = convert_to_timedelta(timeout)
        start_real_time = datetime.datetime.now()
        def calc_delta_time():
            now = datetime.datetime.now()
            diff = now - start_real_time
            return diff
        while True:
            fromLine = _get_last_monitored_line(log_path)
            out = utils.grep_regex_in_line(log_path, grep_regex = regex, match_regex = regex, fromLine = fromLine)
            if len(out) > 0:
                matched = out[-1].matched
                logging.debug(f"{wait_for_regex.__name__}: found {len(out)} matches")
                line_number = out[-1].line_number
                _set_line_number(log_path, line_number)
                if line_number >= fromLine:
                    call(callbacks, "success", line_number, matched[0])
                    return
            diff = calc_delta_time()
            if pause:
                if not diff + pause >= timeout:
                    _sleep(pause)
                else:
                    pause_timeout = timeout - diff
                    _sleep(pause_timeout)
            diff = calc_delta_time()
            if diff > timeout:
                call(callbacks, "timeout", timeout)
                logging.debug(f"{wait_for_regex.__name__}: break {diff} > {timeout} timeout")
                return
    try:
        _init_log_path()
        _pause_monitor(log_path)
        _wait_for_regex()
    finally:
        _resume_monitor(log_path)
