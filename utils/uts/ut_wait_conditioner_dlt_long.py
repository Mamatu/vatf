__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from contextlib import contextmanager
from unittest.mock import patch

import datetime
import os

from vatf.executor import wait
from vatf.executor import shell
from vatf.utils import dlt
from vatf.utils import libcmdringbuffer
from vatf.utils import os_proxy
from vatf.utils import thread_with_stop

_written_lines_count = 0

import time

def generate_lines(lines_count):
    global _written_lines_count
    s = ""
    for line_count in range(_written_lines_count, lines_count + _written_lines_count):
        now = datetime.datetime.now()
        s = f"{s}\n{now} line_{line_count}"
        _written_lines_count = _written_lines_count + 1
    print(s)
    global _lines_in_one_write
    return s, 2, 1

def generate_data():
    return generate_lines(100)

# Source: https://stackoverflow.com/a/46919967
@contextmanager
def mocked_now(now):
    class MockedDatetime(datetime.datetime):
        @classmethod
        def now(cls):
            return now
    with patch("datetime.datetime", MockedDatetime):
        yield

_dlt_daemon = None

def setup_function():
    global _dlt_daemon, _written_lines_count
    _written_lines_count = 0
    _dlt_daemon = dlt.DltDaemon(get_project_path())
    _dlt_daemon.start()

def teardown_function():
    global _dlt_daemon
    _dlt_daemon.stop()

def get_project_path():
    return "/tmp/dlt-project"

def get_receive_path():
    _dlt_project_path = get_project_path()
    _dlt_rootfs = os.path.join(_dlt_project_path, "rootfs")
    _dlt_receive_path = os.path.join(_dlt_rootfs, "bin/dlt-receive")
    return _dlt_receive_path

def _test_wrapper(test_func):
    def inner():
        import tempfile
        writer = dlt.DltWriter(get_project_path())
        tempdir = tempfile.TemporaryDirectory(dir="/tmp")
        try:
            test_func(writer, tempdir)
        except shell.StderrException as ex:
            print(f"Expected StderrException: {ex}")
        except Exception as ex:
            import sys
            print(ex, file=sys.stderr)
            assert False
        finally:
            writer.stop()
            #tempdir.cleanup()
    return inner

@_test_wrapper
def test_libcmdringbuffer_lines_count_1_chunks_count_1(writer, tempdir):
    from vatf.utils import lib_log_snapshot
    from vatf.utils import os_proxy
    chunks_dir = os.path.join(tempdir.name, "chunks")
    try:
        import shutil
        shutil.rmtree(chunks_dir)
    except FileNotFoundError:
        pass
    config = {
        "wait_for_regex.command" : f"{get_receive_path()} -a 127.0.0.1",
        "wait_for_regex.is_file_ring_buffer" : True,
        "wait_for_regex.lines_count" : 1,
        "wait_for_regex.chunks_count" : 1,
        "wait_for_regex.workspace" : f"{tempdir.name}",
        "wait_for_regex.date_format" : "%Y-%m-%d %H:%M:%S.%f",
        "wait_for_regex.date_regex" : "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    }
    wait.start(config = config)
    def target(*args):
        time.sleep(1)
        writer = args[0]
        generate_data = args[1]
        writer.write_in_async_loop(pre_callback = generate_data)
    thread = thread_with_stop.Thread(target = target, args = [writer, generate_data])
    thread.start()
    try:
        assert wait.wait_for_regex("line_3", timeout = 8, config = config)
    finally:
        thread.stop()
        wait.stop()
