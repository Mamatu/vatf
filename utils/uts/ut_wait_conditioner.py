__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import pytest
import logging
from unittest.mock import patch
from vatf.utils import os_proxy

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

def test_start_stop():
    from vatf.utils import config_handler
    config_handler.init_configs("utils/uts/data/ut_config/wait_conditioner_frb_config.json")
    from vatf.utils import wait_conditioner
    wait_conditioner.start()
    wait_conditioner.stop()

def test_check_if_start_point_is_before_time():
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
    text = [
    "2022-01-29 20:54:55.567000 line1\n",
    "2022-01-29 20:54:55.567000 line2\n",
    "2022-01-29 20:54:55.568000 line3\n",
    "2022-01-29 20:54:55.569000 line4\n",
    "2022-01-29 20:54:55.570000 line5\n",
    "2022-01-29 20:54:55.600000 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
    start_point = datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 566000).strftime(date_format)
    from vatf.utils import wait_conditioner as w_cond
    assert w_cond._check_if_start_point_is_before_time(log_file.name, config = config, start_point = start_point)
    log_file.close()

def test_check_if_start_point_is_before_time_fail_1():
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
    text = [
    "2022-01-29 20:54:55.567000 line1\n",
    "2022-01-29 20:54:55.567000 line2\n",
    "2022-01-29 20:54:55.568000 line3\n",
    "2022-01-29 20:54:55.569000 line4\n",
    "2022-01-29 20:54:55.570000 line5\n",
    "2022-01-29 20:54:55.600000 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
    start_point = datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 567000).strftime(date_format)
    from vatf.utils import wait_conditioner as w_cond
    assert not w_cond._check_if_start_point_is_before_time(log_file.name, config = config, start_point = start_point)
    log_file.close()

def test_find_closest_line_number_to_date_1():
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
    text = [
    "2022-01-29 20:54:55.567000 line1\n",
    "2022-01-29 20:54:55.567000 line2\n",
    "2022-01-29 20:54:55.568000 line3\n",
    "2022-01-29 20:54:55.569000 line4\n",
    "2022-01-29 20:54:55.570000 line5\n",
    "2022-01-29 20:54:55.600000 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
    start_point = datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 567100).strftime(date_format)
    from vatf.utils import wait_conditioner as w_cond
    line = w_cond._find_closest_date_greater_than_start_point(log_file.name, config = config, start_point = start_point)
    assert 3 == line.line_number
    log_file.close()

def test_find_closest_line_number_to_date_2():
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
    text = [
    "2022-01-29 20:54:55.567000 line1\n",
    "2022-01-29 20:54:55.567000 line2\n",
    "2022-01-29 20:54:55.568000 line3\n",
    "2022-01-29 20:54:55.569000 line4\n",
    "2022-01-29 20:54:55.570000 line5\n",
    "2022-01-29 20:54:55.600000 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
    start_point = datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 567900).strftime(date_format)
    from vatf.utils import wait_conditioner as w_cond
    line = w_cond._find_closest_date_greater_than_start_point(log_file.name, config = config, start_point = start_point)
    assert 3 == line.line_number
    log_file.close()

def test_check_if_start_point_is_before_time_fail_2():
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
    text = [
    "2022-01-29 20:54:55.567000 line1\n",
    "2022-01-29 20:54:55.567000 line2\n",
    "2022-01-29 20:54:55.568000 line3\n",
    "2022-01-29 20:54:55.569000 line4\n",
    "2022-01-29 20:54:55.570000 line5\n",
    "2022-01-29 20:54:55.600000 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
    start_point = datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 601000).strftime(date_format)
    from vatf.utils import wait_conditioner as w_cond
    assert not w_cond._check_if_start_point_is_before_time(log_file.name, config = config, start_point = start_point)
    log_file.close()

@patch("time.sleep")
def test_handle_in_order_line_pass(time_sleep_mock):
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567000 line1\n",
    "2022-01-29 20:54:55.567000 line2\n",
    "2022-01-29 20:54:55.568000 line3\n",
    "2022-01-29 20:54:55.569000 line4\n",
    "2022-01-29 20:54:55.570000 line5\n",
    "2022-01-29 20:54:55.600000 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    from vatf.utils import wait_conditioner as w_cond
    assert w_cond._handle_in_order_line(["line1", "line3", "line4", "line6", w_cond.RegexOperator.IN_ORDER_LINE], filepath = log_file.name, labels_objects = {})
    log_file.close()

@patch("time.sleep")
def test_handle_in_order_line_fail(time_sleep_mock):
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567000 line1\n",
    "2022-01-29 20:54:55.567000 line2\n",
    "2022-01-29 20:54:55.568000 line3\n",
    "2022-01-29 20:54:55.569000 line4\n",
    "2022-01-29 20:54:55.570000 line5\n",
    "2022-01-29 20:54:55.600000 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    from vatf.utils import wait_conditioner as w_cond
    assert not w_cond._handle_in_order_line(["line3", "line1", "line4", "line6", w_cond.RegexOperator.IN_ORDER_LINE], filepath = log_file.name, labels_objects = {})
    log_file.close()

@patch("time.sleep")
def test_handle_and_pass(time_sleep_mock):
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567000 line1\n",
    "2022-01-29 20:54:55.567000 line2\n",
    "2022-01-29 20:54:55.568000 line3\n",
    "2022-01-29 20:54:55.569000 line4\n",
    "2022-01-29 20:54:55.570000 line5\n",
    "2022-01-29 20:54:55.600000 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    from vatf.utils import wait_conditioner as w_cond
    assert w_cond._handle_and(["line6", "line3", "line4", "line1", w_cond.RegexOperator.AND], filepath = log_file.name, labels_objects = {})
    log_file.close()

@patch("time.sleep")
def test_handle_and_fail(time_sleep_mock):
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567000 line1\n",
    "2022-01-29 20:54:55.567000 line2\n",
    "2022-01-29 20:54:55.568000 line3\n",
    "2022-01-29 20:54:55.569000 line4\n",
    "2022-01-29 20:54:55.570000 line5\n",
    "2022-01-29 20:54:55.600000 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    from vatf.utils import wait_conditioner as w_cond
    assert not w_cond._handle_and(["line6", "line3", "line4", "line15", w_cond.RegexOperator.AND], filepath = log_file.name, labels_objects = {})
    log_file.close()

@patch("time.sleep")
def test_handle_or_pass(time_sleep_mock):
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567000 line1\n",
    "2022-01-29 20:54:55.567000 line2\n",
    "2022-01-29 20:54:55.568000 line3\n",
    "2022-01-29 20:54:55.569000 line4\n",
    "2022-01-29 20:54:55.570000 line5\n",
    "2022-01-29 20:54:55.600000 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    from vatf.utils import wait_conditioner as w_cond
    assert w_cond._handle_or(["line15", "line16", "line17", "line1", w_cond.RegexOperator.OR], filepath = log_file.name, labels_objects = {})
    log_file.close()

@patch("time.sleep")
def test_handle_or_fail(time_sleep_mock):
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567000 line1\n",
    "2022-01-29 20:54:55.567000 line2\n",
    "2022-01-29 20:54:55.568000 line3\n",
    "2022-01-29 20:54:55.569000 line4\n",
    "2022-01-29 20:54:55.570000 line5\n",
    "2022-01-29 20:54:55.600000 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    from vatf.utils import wait_conditioner as w_cond
    assert not w_cond._handle_or(["line15", "line16", "line17", "line18", w_cond.RegexOperator.OR], filepath = log_file.name, labels_objects = {})
    log_file.close()

@patch("time.sleep")
def test_wait_for_regex_1(time_sleep_mock):
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 566000)):
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
        time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
        text = [
        "2022-01-29 20:54:55.567000 line1\n",
        "2022-01-29 20:54:55.567000 line2\n",
        "2022-01-29 20:54:55.568000 line3\n",
        "2022-01-29 20:54:55.569000 line4\n",
        "2022-01-29 20:54:55.570000 line5\n",
        "2022-01-29 20:54:55.600000 line6\n",
        ]
        log_file = os_proxy.create_tmp_file("w", data = "".join(text))
        config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
        from vatf.utils import wait_conditioner as w_cond
        assert w_cond.wait_for_regex(["line1", "line3", "line5", "line6", w_cond.RegexOperator.IN_ORDER_LINE], timeout = 0.1, config = config)
        log_file.close()

@patch("time.sleep")
def test_wait_for_regex_2(time_sleep_mock):
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 566)):
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
        time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
        text = [
        "2022-01-29 20:54:55.567000 line1\n",
        "2022-01-29 20:54:55.567000 line2\n",
        "2022-01-29 20:54:55.568000 line3\n",
        "2022-01-29 20:54:55.569000 line4\n",
        "2022-01-29 20:54:55.570000 line5\n",
        "2022-01-29 20:54:55.600000 line6\n",
        ]
        log_file = os_proxy.create_tmp_file("w", data = "".join(text))
        config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
        from vatf.utils import wait_conditioner as w_cond
        assert not w_cond.wait_for_regex(["line15", "line16", "line17", "line18", w_cond.RegexOperator.OR], timeout = 0.1, config = config)
        log_file.close()

@patch("time.sleep")
def test_wait_for_regex_3(time_sleep_mock):
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 566)):
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
        time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
        text = [
        "2022-01-29 20:54:55.567000 line1\n",
        "2022-01-29 20:54:55.567000 line2\n",
        "2022-01-29 20:54:55.568000 line3\n",
        "2022-01-29 20:54:55.569000 line4\n",
        "2022-01-29 20:54:55.570000 line5\n",
        "2022-01-29 20:54:55.600000 line6\n",
        ]
        log_file = os_proxy.create_tmp_file("w", data = "".join(text))
        config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
        from vatf.utils import wait_conditioner as w_cond
        assert w_cond.wait_for_regex(["line1", ["line3", "line15", w_cond.RegexOperator.AND], w_cond.RegexOperator.OR], timeout = 0.1, config = config)
        log_file.close()

@patch("time.sleep")
def test_wait_for_regex_3_labels(time_sleep_mock):
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 566)):
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
        time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
        text = [
        "2022-01-29 20:54:55.567000 line1\n",
        "2022-01-29 20:54:55.567000 line2\n",
        "2022-01-29 20:54:55.568000 line3\n",
        "2022-01-29 20:54:55.569000 line4\n",
        "2022-01-29 20:54:55.570000 line5\n",
        "2022-01-29 20:54:55.600000 line6\n",
        ]
        log_file = os_proxy.create_tmp_file("w", data = "".join(text))
        config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
        labels = {}
        from vatf.utils import wait_conditioner as w_cond
        assert w_cond.wait_for_regex(["line1", w_cond.Label("cond_1"), ["line3", w_cond.Label("cond_2"), "line15", w_cond.Label("cond_3"), w_cond.RegexOperator.AND], w_cond.RegexOperator.OR], timeout = 0.1, config = config, labels = labels)
        assert labels["cond_1"] is True
        assert labels["cond_2"] is False 
        assert labels["cond_3"] is False 
        log_file.close()

@patch("time.sleep")
def test_wait_for_regex_4(time_sleep_mock):
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 567000)):
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
        time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
        text = [
        "2022-01-29 20:54:55.567000 line1\n",
        "2022-01-29 20:54:55.567000 line2\n",
        "2022-01-29 20:54:55.568000 line3\n",
        "2022-01-29 20:54:55.569000 line4\n",
        "2022-01-29 20:54:55.570000 line5\n",
        "2022-01-29 20:54:55.600000 line6\n",
        ]
        log_file = os_proxy.create_tmp_file("w", data = "".join(text))
        config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
        from vatf.utils import wait_conditioner as w_cond
        assert not w_cond.wait_for_regex(["line1", ["line3", "line15", w_cond.RegexOperator.AND], w_cond.RegexOperator.IN_ORDER_LINE], timeout = 0.1, config = config)
        log_file.close()

@patch("time.sleep")
def test_wait_for_regex_4_labels(time_sleep_mock):
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 567000)):
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
        time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
        text = [
        "2022-01-29 20:54:55.567000 line1\n",
        "2022-01-29 20:54:55.567000 line2\n",
        "2022-01-29 20:54:55.568000 line3\n",
        "2022-01-29 20:54:55.569000 line4\n",
        "2022-01-29 20:54:55.570000 line5\n",
        "2022-01-29 20:54:55.600000 line6\n",
        ]
        log_file = os_proxy.create_tmp_file("w", data = "".join(text))
        config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
        labels = {}
        from vatf.utils import wait_conditioner as w_cond
        assert not w_cond.wait_for_regex(["line1", w_cond.Label("cond_1"), ["line3", "line15", w_cond.Label("cond_2"), w_cond.RegexOperator.AND], w_cond.RegexOperator.IN_ORDER_LINE], timeout = 0.1, config = config, labels = labels)
        assert labels["cond_2"] is False
        assert labels["cond_1"] is False
        log_file.close()

@patch("time.sleep")
def test_wait_for_regex_simple_label(time_sleep_mock):
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 566000)):
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
        time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
        text = [
        "2022-01-29 20:54:55.567000 line1\n",
        "2022-01-29 20:54:55.567000 line2\n",
        "2022-01-29 20:54:55.568000 line3\n",
        "2022-01-29 20:54:55.569000 line4\n",
        "2022-01-29 20:54:55.570000 line5\n",
        "2022-01-29 20:54:55.600000 line6\n",
        ]
        log_file = os_proxy.create_tmp_file("w", data = "".join(text))
        config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
        labels = {}
        from vatf.utils import wait_conditioner as w_cond
        assert w_cond.wait_for_regex(["line1", w_cond.RegexOperator.IN_ORDER_LINE, w_cond.Label("condition_1")], timeout = 0.1, config = config, labels = labels)
        assert "condition_1" in labels
        assert labels["condition_1"] is True
        log_file.close()

@patch("time.sleep")
def test_wait_for_single_regex_pass(time_sleep_mock):
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 566000)):
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
        time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
        text = [
        "2022-01-29 20:54:55.567000 line1\n",
        "2022-01-29 20:54:55.567000 line2\n",
        "2022-01-29 20:54:55.568000 line3\n",
        "2022-01-29 20:54:55.569000 line4\n",
        "2022-01-29 20:54:55.570000 line5\n",
        "2022-01-29 20:54:55.600000 line6\n",
        ]
        log_file = os_proxy.create_tmp_file("w", data = "".join(text))
        config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
        from vatf.utils import wait_conditioner as w_cond
        assert w_cond.wait_for_regex("line1", timeout = 0.1, config = config)
        log_file.close()

@patch("time.sleep")
def test_wait_for_single_regex_fail(time_sleep_mock):
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 566000)):
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
        time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
        text = [
        "2022-01-29 20:54:55.567000 line1\n",
        "2022-01-29 20:54:55.567000 line2\n",
        "2022-01-29 20:54:55.568000 line3\n",
        "2022-01-29 20:54:55.569000 line4\n",
        "2022-01-29 20:54:55.570000 line5\n",
        "2022-01-29 20:54:55.600000 line6\n",
        ]
        log_file = os_proxy.create_tmp_file("w", data = "".join(text))
        config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
        from vatf.utils import wait_conditioner as w_cond
        assert not w_cond.wait_for_regex("line7", timeout = 0.1, config = config)
        log_file.close()

@patch("time.sleep")
def test_wait_for_single_regex_pass_in_tuple(time_sleep_mock):
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 566000)):
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
        time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
        text = [
        "2022-01-29 20:54:55.567000 line1\n",
        "2022-01-29 20:54:55.567000 line2\n",
        "2022-01-29 20:54:55.568000 line3\n",
        "2022-01-29 20:54:55.569000 line4\n",
        "2022-01-29 20:54:55.570000 line5\n",
        "2022-01-29 20:54:55.600000 line6\n",
        ]
        log_file = os_proxy.create_tmp_file("w", data = "".join(text))
        config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
        from vatf.utils import wait_conditioner as w_cond
        assert w_cond.wait_for_regex(("line1",), timeout = 0.1, config = config)
        log_file.close()

@patch("time.sleep")
def test_wait_for_single_regex_fail_in_tuple(time_sleep_mock):
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 567000)):
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
        time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
        text = [
        "2022-01-29 20:54:55.567000 line1\n",
        "2022-01-29 20:54:55.567000 line2\n",
        "2022-01-29 20:54:55.568000 line3\n",
        "2022-01-29 20:54:55.569000 line4\n",
        "2022-01-29 20:54:55.570000 line5\n",
        "2022-01-29 20:54:55.600000 line6\n",
        ]
        log_file = os_proxy.create_tmp_file("w", data = "".join(text))
        config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
        from vatf.utils import wait_conditioner as w_cond
        assert not w_cond.wait_for_regex(("line7",), timeout = 0.1, config = config)
        log_file.close()

@patch("time.sleep")
def test_wait_for_single_regex_from_start_point_pass(time_sleep_mock):
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 570000)):
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
        time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
        text = [
        "2022-01-29 20:54:55.567000 line1\n",
        "2022-01-29 20:54:55.567000 line2\n",
        "2022-01-29 20:54:55.568000 line3\n",
        "2022-01-29 20:54:55.569000 line4\n",
        "2022-01-29 20:54:55.570000 line5\n",
        "2022-01-29 20:54:55.600000 line1\n",
        ]
        log_file = os_proxy.create_tmp_file("w", data = "".join(text))
        config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
        labels = {}
        from vatf.utils import wait_conditioner as w_cond
        assert w_cond.wait_for_regex(["line1", w_cond.Label("cond_1")], timeout = 0.1, config = config, labels = labels)
        assert labels["cond_1"]
        log_file.close()

@patch("time.sleep")
def test_wait_for_single_regex_from_start_point_fail(time_sleep_mock):
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 570000)):
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
        time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
        text = [
        "2022-01-29 20:54:55.567000 line1\n",
        "2022-01-29 20:54:55.567000 line2\n",
        "2022-01-29 20:54:55.568000 line3\n",
        "2022-01-29 20:54:55.569000 line4\n",
        "2022-01-29 20:54:55.570000 line5\n",
        "2022-01-29 20:54:55.600000 line6\n",
        ]
        log_file = os_proxy.create_tmp_file("w", data = "".join(text))
        config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
        labels = {}
        from vatf.utils import wait_conditioner as w_cond
        assert not w_cond.wait_for_regex(["line1", w_cond.Label("cond_1")], timeout = 0.1, config = config, labels = labels)
        assert not labels["cond_1"]
        log_file.close()

@patch("time.sleep")
def test_wait_for_regex_duplicated_label_exception(time_sleep_mock):
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 570000)):
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
        time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
        text = [
        "2022-01-29 20:54:55.567000 line1\n",
        "2022-01-29 20:54:55.567000 line2\n",
        "2022-01-29 20:54:55.568000 line3\n",
        "2022-01-29 20:54:55.569000 line4\n",
        "2022-01-29 20:54:55.570000 line5\n",
        "2022-01-29 20:54:55.600000 line6\n",
        ]
        log_file = os_proxy.create_tmp_file("w", data = "".join(text))
        config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
        labels = {}
        is_exception = False
        try:
            from vatf.utils import wait_conditioner as w_cond
            assert not w_cond.wait_for_regex([["line1", w_cond.Label("cond_1")], "line2", w_cond.Label("cond_1")], timeout = 0.1, config = config, labels = labels)
            assert not labels["cond_1"]
        except:
            is_exception = True
        assert is_exception
        log_file.close()

@patch("time.sleep")
def test_wait_for_sequence_of_fails(time_sleep_mock):
    text = [
    "2022-01-29 20:54:55.567000 line1\n",
    "2022-01-29 20:54:55.567000 line2\n",
    ]
    text1 = [
    "2022-01-29 20:54:55.568000 line1\n",
    "2022-01-29 20:54:55.569000 line4\n",
    ]
    text2 = [
    "2022-01-29 20:54:55.570000 line1\n",
    "2022-01-29 20:54:55.600000 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
    config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 567001)):
        time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
        labels = {}
        from vatf.utils import wait_conditioner as w_cond
        assert not w_cond.wait_for_regex(["line1", w_cond.Label("cond_1")], timeout = 0.1, config = config, labels = labels)
        assert not labels["cond_1"]
    log_file.write("".join(text1))
    log_file.flush()
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 568001)):
        time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
        labels = {}
        from vatf.utils import wait_conditioner as w_cond
        assert not w_cond.wait_for_regex(["line1", w_cond.Label("cond_1")], timeout = 0.1, config = config, labels = labels)
        assert not labels["cond_1"]
    log_file.write("".join(text2))
    log_file.flush()
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 571001)):
        time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
        labels = {}
        from vatf.utils import wait_conditioner as w_cond
        assert not w_cond.wait_for_regex("line1", timeout = 0.1, config = config, labels = labels)
    log_file.close()

@patch("time.sleep")
def test_wait_for_regex_in_order_two_the_same_regex(time_sleep_mock):
    with mocked_now(datetime.datetime(2022, 1, 29, hour = 20, minute = 54, second = 55, microsecond = 566000)):
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9].[0-9]\\{3\\}"
        time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
        text = [
        "2022-01-29 20:54:55.567000 line1\n",
        "2022-01-29 20:54:55.567000 line2\n",
        "2022-01-29 20:54:55.568000 line1\n",
        "2022-01-29 20:54:55.569000 line4\n",
        "2022-01-29 20:54:55.570000 line5\n",
        "2022-01-29 20:54:55.600000 line6\n",
        ]
        log_file = os_proxy.create_tmp_file("w", data = "".join(text))
        config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
        from vatf.utils import wait_conditioner as w_cond
        assert w_cond.wait_for_regex(["line1", "line2", w_cond.RegexOperator.IN_ORDER_LINE], timeout = 0.1, config = config)
        log_file.close()
