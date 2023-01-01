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
    from vatf.executor import lib_log_snapshot
    snapshot = lib_log_snapshot.make()
    try:
        with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 570000)):
            from vatf.utils import os_proxy
            text = [
                "2022-01-29 20:54:55.567 line1\n",
                "2022-01-29 20:54:55.567 line2\n",
                "2022-01-29 20:54:55.568 line3\n",
                "2022-01-29 20:54:55.569 line4\n",
                "2022-01-29 20:54:55.570 line5\n",
                "2022-01-29 20:54:55.600 line6\n",
            ]
            file = os_proxy.create_tmp_file("w+", data = "".join(text))
            file1 = os_proxy.create_tmp_file("r")
            snapshot.start_copy(file1.name, file.name, timestamp_format = "%Y-%m-%d %H:%M:%S.%f", timestamp_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-9]:[0-6][0-9]:[0-6][0-9].[0-9][0-9][0-9]")
            from vatf.utils import loop
            def cond():
                with open(file1.name, "r") as f:
                    return len(f.readlines()) == 2
            loop.wait_until(cond, pause = 0.1, timeout = 1)
            snapshot.stop()
            with open(file1.name, "r") as f:
                lines = f.readlines()
                assert len(lines) == 2
                assert lines[0] == text[-2]
                assert lines[1] == text[-1]
    finally:
        snapshot.stop()
