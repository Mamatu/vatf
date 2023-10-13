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

_written_lines_count = 0

def generate_line():
    global _written_lines_count
    now = datetime.datetime.now()
    s = f"{now} line_{_written_lines_count}"
    print(s)
    _written_lines_count = _written_lines_count + 1
    global _lines_in_one_write
    return s, 2, 1

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
    global _dlt_daemon
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

def test_libcmdringbuffer():
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 54, microsecond = 000000)):
        from vatf.utils import lib_log_snapshot
        writer = dlt.DltWriter(get_project_path())
        writer_t = None
        #command = f"{get_receive_path()} -a 127.0.0.1 | grep 'LOG- TEST'"
        command = f"{get_receive_path()} -a 127.0.0.1"
        import tempfile
        from vatf.utils import os_proxy
        tempdir = tempfile.TemporaryDirectory(dir="/tmp")
        chunks_dir = os.path.join(tempdir.name, "chunks")
        try:
            import shutil
            shutil.rmtree(chunks_dir)
        except FileNotFoundError:
            pass
        fb = libcmdringbuffer.make(command, os.path.join(tempdir.name, "fifo"), chunks_dir, 100, 2)
        try:
            fb.start()
            writer_t = writer.write_in_async_loop(pre_callback = generate_line)
            wait.sleep(20)
            writer_t.stop()
            fb.stop()
        except shell.StderrException as ex:
            print(f"Expected StderrException: {ex}")
        except Exception as ex:
            import sys
            print(ex, file=sys.stderr)
            assert False
        finally:
            tempdir.cleanup()
