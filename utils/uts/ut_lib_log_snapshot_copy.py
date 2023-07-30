__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from contextlib import contextmanager
from unittest.mock import patch

import datetime

# Source: https://stackoverflow.com/a/46919967
@contextmanager
def mocked_now(now):
    class MockedDatetime(datetime.datetime):
        @classmethod
        def now(cls):
            return now
    with patch("datetime.datetime", MockedDatetime):
        yield

def test_log_copy():
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 570000)):
        from vatf.utils import lib_log_snapshot
        snapshot = lib_log_snapshot.make()
        try:
            from vatf.utils import os_proxy
            text = [
                "2022-01-29 20:54:55.567000 line1\n",
                "2022-01-29 20:54:55.567000 line2\n",
                "2022-01-29 20:54:55.568000 line3\n",
                "2022-01-29 20:54:55.569000 line4\n",
                "2022-01-29 20:54:55.570000 line5\n",
                "2022-01-29 20:54:55.600000 line6\n",
            ]
            file = os_proxy.create_tmp_file("w+", data = "".join(text))
            file1 = os_proxy.create_tmp_file("r")
            snapshot.start_copy(file1.name, file.name, timestamp_format = "%Y-%m-%d %H:%M:%S.%f", timestamp_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-9]:[0-6][0-9]:[0-6][0-9].[0-9][0-9][0-9]")
            from vatf.utils import loop
            def cond():
                with open(file1.name, "r") as f:
                    return len(f.readlines()) == 2
            loop.wait_until_true(cond, pause = 0.1, timeout = 1)
            snapshot.stop()
            assert text[4].strip() == snapshot.get_the_first_line()
            assert text[-1].strip() == snapshot.get_the_last_line()
            assert 2 == snapshot.get_lines_count()
            with open(file1.name, "r") as f:
                lines = f.readlines()
                assert len(lines) == 2
                assert lines[0] == text[-2]
                assert lines[1] == text[-1]
        finally:
            snapshot.stop()

def test_log_copy_get_seconds():
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 54, microsecond = 000000)):
        from vatf.utils import lib_log_snapshot
        snapshot = lib_log_snapshot.make()
        try:
            from vatf.utils import os_proxy
            text = [
                "2022-01-29 20:54:55.000000 line1\n",
                "2022-01-29 20:54:56.000000 line2\n",
                "2022-01-29 20:54:57.000000 line3\n",
                "2022-01-29 20:54:58.000000 line4\n",
                "2022-01-29 20:54:59.000000 line5\n",
                "2022-01-29 20:55:00.000000 line6\n",
            ]
            file = os_proxy.create_tmp_file("w+", data = "".join(text))
            file1 = os_proxy.create_tmp_file("r")
            snapshot.start_copy(file1.name, file.name, timestamp_format = "%Y-%m-%d %H:%M:%S.%f", timestamp_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-9]:[0-6][0-9]:[0-6][0-9].[0-9][0-9][0-9]")
            from vatf.utils import loop
            def cond():
                return snapshot.get_seconds() < 5
            loop.wait_until_true(cond, pause = 0.1, timeout = 1)
            snapshot.stop()
            assert snapshot.get_seconds() == 5
        finally:
            snapshot.stop()

#def test_log_copy_ring_buffer_seconds():
#    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 54, microsecond = 000000)):
#        from vatf.utils import lib_log_snapshot
#        snapshot = lib_log_snapshot.make()
#        try:
#            from vatf.utils import os_proxy
#            text = [
#                "2022-01-29 20:54:55.000000 line1\n",
#                "2022-01-29 20:54:56.000000 line2\n",
#                "2022-01-29 20:54:57.000000 line3\n",
#                "2022-01-29 20:54:58.000000 line4\n",
#                "2022-01-29 20:54:59.000000 line5\n",
#                "2022-01-29 20:55:00.000000 line6\n",
#                "2022-01-29 20:55:01.000000 line7\n",
#                "2022-01-29 20:55:02.000000 line8\n",
#                "2022-01-29 20:55:03.000000 line9\n",
#                "2022-01-29 20:55:04.000000 line10\n",
#                "2022-01-29 20:55:05.000000 line11\n",
#                "2022-01-29 20:55:06.000000 line12\n",
#                "2022-01-29 20:55:07.000000 line13\n",
#                "2022-01-29 20:55:08.000000 line14\n",
#                "2022-01-29 20:55:09.000000 line15\n",
#                "2022-01-29 20:56:00.000000 line16\n",
#            ]
#            file = os_proxy.create_tmp_file("w+", data = "".join(text))
#            file1 = os_proxy.create_tmp_file("r")
#            snapshot.set_ring_buffer(length_in_seconds = 5)
#            snapshot.start_copy(file1.name, file.name, timestamp_format = "%Y-%m-%d %H:%M:%S.%f", timestamp_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-9]:[0-6][0-9]:[0-6][0-9].[0-9][0-9][0-9]")
#            from vatf.utils import loop
#            def cond():
#                return snapshot.get_the_last_line() == "2022-01-29 20:56:00.000000 line16" and snapshot.get_ring_buffer_count() > 0
#            assert loop.wait_until_true(cond, pause = 0.1, timeout = 4)
#            with open(file1.name, "r") as f:
#                lines = f.readlines()
#                assert len(lines) == 5
#        finally:
#            snapshot.stop()
