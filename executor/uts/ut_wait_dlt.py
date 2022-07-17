import errno
import datetime
import logging
import textwrap
import time
import threading
import os

import sys

from vatf.executor import log_snapshot, shell, wait
from vatf.utils import utils

_counter = None
_generated_lines = []
_dlt_daemon = None
_dlt_project = "/tmp/dlt-project"
_dlt_rootfs = os.path.join(_dlt_project, "rootfs")
_dlt_example_user_path = os.path.join(_dlt_rootfs, "bin/dlt-example-user")
_dlt_receive_path = os.path.join(_dlt_rootfs, "bin/dlt-receive")
_dlt_daemon_path = os.path.join(_dlt_rootfs, "bin/dlt-daemon")

_generator_thread = None

def _dlt(command):
    global _dlt_rootfs
    return os.path.join(_dlt_rootfs, command)

def _dlt_example_user(payload, log_level = 2, count = 1):
    global _dlt_example_user_path
    os.system(f"LD_LIBRARY_PATH={_dlt_rootfs}/lib {_dlt_example_user_path} -n {count} -d 0 \"{payload}\"")

from vatf.utils import debug

def setup_module():
    from vatf import vatf_api
    vatf_api.set_api_type(vatf_api.API_TYPE.EXECUTOR)
    global _dlt_daemon_path
    global _dlt_daemon
    if not _dlt_daemon is None:
        raise Exception("dlt deamon is run! It should be not")
    _dlt_daemon = shell.bg(_dlt_daemon_path, shell = False)

def teardown_module():
    global _dlt_daemon, _generator_thread
    if not _generator_thread:
        raise Exception("log generator is not running")
    _generator_thread.stop()
    _generator_thread.join()
    shell.kill(_dlt_daemon)
    _dlt_daemon = None

_test_end_indicator = "test end"

def _log_generator_run(log_path, lines_count, custom_sleep = None):
    global _generator_thread, _test_end_indicator
    class GeneratorThread(threading.Thread):
        def __init__(self, filepath, lines, custom_sleep):
            threading.Thread.__init__(self)
            self.stopped = False
        def stop(self):
            self.stopped = True
        def run(self):
            threading.Thread.run(self)
            global _counter, _generated_lines, _dlt_daemon
            if not _counter:
                _counter = 0
            while _counter < lines_count and not self.stopped:
                line = f"line{_counter + 1}"
                now = datetime.datetime.now()
                line = f"{now} {line}"
                _generated_lines.append(line)
                _dlt_example_user(line, count = 100)
                it = None
                if self.stopped:
                    break
                if custom_sleep:
                    sleep_duration = custom_sleep.get(_counter)
                    if sleep_duration:
                        time.sleep(sleep_duration)
                _counter = _counter + 1
    _generator_thread = GeneratorThread(log_path, lines_count, custom_sleep)
    _generator_thread.start()

def test_wait_for_regex():
    try:
        global _generated_lines, _dlt_receive_path, _test_end_indicator
        log_path = utils.get_temp_filepath()
        print(f"DLT -> {log_path}")
        lines_count = 10
        utils.touch(log_path)
        _log_generator_run(log_path, lines_count)
        from functools import partial
        command = f"{_dlt_receive_path} -a 127.0.0.1 | grep 'LOG- TEST' > {log_path}"
        command1 = str(_dlt_receive_path) + " -a 127.0.0.1 | grep 'LOG- TEST' > {log_path}"
        log_snapshot.start(log_path, command)
        assert True == wait.wait_for_regex("line2", config_attrs = {"wait_for_regex.command" : command1})
        log_snapshot.stop()
        lines = []
        with open(log_path, "r") as f:
            lines = f.readlines()
        def expected(line, is_last):
            global _generated_lines
            for gline in _generated_lines:
                if gline in line:
                    return True
                if _test_end_indicator in line:
                    return True
            if is_last:
                return True
            return False
        not_expected = [x for x in lines if not expected(x, lines.index(x) == len(lines) - 1)]
        assert 0 == len(not_expected)
    except Exception as ex:
        print(ex, file=sys.stderr)
        assert False
