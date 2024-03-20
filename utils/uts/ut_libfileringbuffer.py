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
from vatf.utils import libfileringbuffer
from vatf.utils import os_proxy

import time

def generate_lines(lines_count):
    s = [f"line_{x}" for x in range(0, lines_count)]
    return "\n".join(s)

def generate_and_write_lines(path, lines_count):
    with open(path, "w") as f:
        data = generate_lines(lines_count)
        f.write(data)
        f.flush()

# Source: https://stackoverflow.com/a/46919967
@contextmanager
def mocked_now(now):
    class MockedDatetime(datetime.datetime):
        @classmethod
        def now(cls):
            return now
    with patch("datetime.datetime", MockedDatetime):
        yield

def get_file_content(path):
    with open(path, "r") as f:
        return f.read()

def print_chunk(chunks_dir, chunk):
    path = os.path.join(chunks_dir, chunk)
    with open(path, "r") as f:
        print(f"FILE: {path}")
        print(f.read())

def expect_lines(chunks_dir, chunk, _min, _max, extra = ""):
    path = os.path.join(chunks_dir, chunk)
    with open(path, "r") as f:
        data = f.read()
        expected_data = [f"line_{x}" for x in range(_min, _max + 1)]
        expected_data = "\n".join(expected_data)
        expected_data = f"{expected_data}{extra}"
        assert data == expected_data

def test_libcmdringbuffer_1():
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 54, microsecond = 000000)):
        from vatf.utils import lib_log_snapshot
        import tempfile
        from vatf.utils import os_proxy
        with tempfile.TemporaryDirectory(dir="/tmp") as tempdir:
            chunks_dir = os.path.join(tempdir, "chunks")
            fifo_path = os.path.join(tempdir, "fifo")
            crb = libfileringbuffer.make(fifo_path, chunks_dir, 100, 3, timestamp_lock = False)
            crb.start()
            generate_and_write_lines(fifo_path, 300)
            time.sleep(2)
            chunks_list = os.listdir(chunks_dir)
            chunks_list.sort()
            assert chunks_list == ["0", "1", "2"]
            expect_lines(chunks_dir, "0", 0, 99, "\n")
            expect_lines(chunks_dir, "1", 100, 199, "\n")
            expect_lines(chunks_dir, "2", 200, 299)
            crb.stop()

def test_libcmdringbuffer_2():
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 54, microsecond = 000000)):
        from vatf.utils import lib_log_snapshot
        import tempfile
        from vatf.utils import os_proxy
        with tempfile.TemporaryDirectory(dir="/tmp") as tempdir:
            chunks_dir = os.path.join(tempdir, "chunks")
            fifo_path = os.path.join(tempdir, "fifo")
            crb = libfileringbuffer.make(fifo_path, chunks_dir, 100, 3, timestamp_lock = False)
            crb.start()
            generate_and_write_lines(fifo_path, 400)
            time.sleep(10)
            chunks_list = os.listdir(chunks_dir)
            chunks_list.sort()
            try:
                assert chunks_list == ["1", "2", "3"]
            finally:
                crb.stop()

def test_libcmdringbuffer_2_keep_files():
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 54, microsecond = 000000)):
        from vatf.utils import lib_log_snapshot
        import tempfile
        from vatf.utils import os_proxy
        with tempfile.TemporaryDirectory(dir="/tmp") as tempdir:
            chunks_dir = os.path.join(tempdir, "chunks")
            fifo_path = os.path.join(tempdir, "fifo")
            crb = libfileringbuffer.make(fifo_path, chunks_dir, 100, 3, keep_files = True, timestamp_lock = False)
            crb.start()
            generate_and_write_lines(fifo_path, 400)
            time.sleep(10)
            chunks_list = os.listdir(chunks_dir)
            chunks_list.sort()
            try:
                assert chunks_list == ["0", "1", "2", "3"]
            finally:
                crb.stop()

def test_libcmdringbuffer_3():
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 54, microsecond = 000000)):
        from vatf.utils import lib_log_snapshot
        import tempfile
        from vatf.utils import os_proxy
        with tempfile.TemporaryDirectory(dir="/tmp") as tempdir:
            chunks_dir = os.path.join(tempdir, "chunks")
            fifo_path = os.path.join(tempdir, "fifo")
            crb = libfileringbuffer.make(fifo_path, chunks_dir, 100, 3, timestamp_lock = False)
            crb.start()
            generate_and_write_lines(fifo_path, 900)
            time.sleep(2)
            chunks_list = os.listdir(chunks_dir)
            chunks_list.sort()
            assert chunks_list == ["6", "7", "8"]
            crb.stop()

def test_libcmdringbuffer_3_keep_files():
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 54, microsecond = 000000)):
        from vatf.utils import lib_log_snapshot
        import tempfile
        from vatf.utils import os_proxy
        with tempfile.TemporaryDirectory(dir="/tmp") as tempdir:
            chunks_dir = os.path.join(tempdir, "chunks")
            fifo_path = os.path.join(tempdir, "fifo")
            crb = libfileringbuffer.make(fifo_path, chunks_dir, 100, 3, keep_files = True, timestamp_lock = False)
            crb.start()
            generate_and_write_lines(fifo_path, 900)
            time.sleep(2)
            chunks_list = os.listdir(chunks_dir)
            chunks_list.sort()
            assert chunks_list == ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
            crb.stop()
