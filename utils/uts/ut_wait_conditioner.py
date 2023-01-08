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
from vatf.utils import wait_conditioner as w_cond

@patch("time.sleep")
def test_handle_in_order_line_pass(time_sleep_mock):
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    assert w_cond._handle_in_order_line(["line1", "line3", "line4", "line6", w_cond.RegexOperator.IN_ORDER_LINE], filepath = log_file.name)
    log_file.close()

@patch("time.sleep")
def test_handle_in_order_line_fail(time_sleep_mock):
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    assert not w_cond._handle_in_order_line(["line3", "line1", "line4", "line6", w_cond.RegexOperator.IN_ORDER_LINE], filepath = log_file.name)
    log_file.close()

@patch("time.sleep")
def test_handle_and_pass(time_sleep_mock):
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    assert w_cond._handle_and(["line6", "line3", "line4", "line1", w_cond.RegexOperator.AND], filepath = log_file.name)
    log_file.close()

@patch("time.sleep")
def test_handle_and_fail(time_sleep_mock):
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    assert not w_cond._handle_and(["line6", "line3", "line4", "line15", w_cond.RegexOperator.AND], filepath = log_file.name)
    log_file.close()

@patch("time.sleep")
def test_handle_or_pass(time_sleep_mock):
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    assert w_cond._handle_or(["line15", "line16", "line17", "line1", w_cond.RegexOperator.OR], filepath = log_file.name)
    log_file.close()

@patch("time.sleep")
def test_handle_or_fail(time_sleep_mock):
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    assert not w_cond._handle_or(["line15", "line16", "line17", "line18", w_cond.RegexOperator.OR], filepath = log_file.name)
    log_file.close()

@patch("time.sleep")
def test_wait_for_regex_1(time_sleep_mock):
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9"
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
    assert w_cond.wait_for_regex(["line1", "line3", "line5", "line6", w_cond.RegexOperator.IN_ORDER_LINE], timeout = 0.1, config = config)
    log_file.close()

@patch("time.sleep")
def test_wait_for_regex_2(time_sleep_mock):
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9"
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
    assert not w_cond.wait_for_regex(["line15", "line16", "line17", "line18", w_cond.RegexOperator.OR], timeout = 0.1, config = config)
    log_file.close()

@patch("time.sleep")
def test_wait_for_regex_3(time_sleep_mock):
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9]"
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
    assert w_cond.wait_for_regex(["line1", ["line3", "line15", w_cond.RegexOperator.AND], w_cond.RegexOperator.OR], timeout = 0.1, config = config)
    log_file.close()

@patch("time.sleep")
def test_wait_for_regex_3_labels(time_sleep_mock):
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9]"
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
    labels = {}
    assert w_cond.wait_for_regex(["line1", w_cond.Label("cond_1"), ["line3", w_cond.Label("cond_2"), "line15", w_cond.Label("cond_3"), w_cond.RegexOperator.AND], w_cond.RegexOperator.OR], timeout = 0.1, config = config, labels = labels)
    assert labels["cond_1"] is True
    assert labels["cond_2"] is False 
    assert labels["cond_3"] is False 
    log_file.close()

@patch("time.sleep")
def test_wait_for_regex_4(time_sleep_mock):
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9"
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
    assert not w_cond.wait_for_regex(["line1", ["line3", "line15", w_cond.RegexOperator.AND], w_cond.RegexOperator.IN_ORDER_LINE], timeout = 0.1, config = config)
    log_file.close()

@patch("time.sleep")
def test_wait_for_regex_4_labels(time_sleep_mock):
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9"
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
    labels = {}
    assert not w_cond.wait_for_regex(["line1", w_cond.Label("cond_1"), ["line3", "line15", w_cond.Label("cond_2"), w_cond.RegexOperator.AND], w_cond.RegexOperator.IN_ORDER_LINE], timeout = 0.1, config = config, labels = labels)
    assert labels["cond_2"] is False
    assert labels["cond_1"] is False
    log_file.close()

@patch("time.sleep")
def test_wait_for_regex_simple_label(time_sleep_mock):
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9"
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
    labels = {}
    assert w_cond.wait_for_regex(["line1", w_cond.RegexOperator.IN_ORDER_LINE, w_cond.Label("condition_1")], timeout = 0.1, config = config, labels = labels)
    assert "condition_1" in labels
    assert labels["condition_1"] is True
    log_file.close()

@patch("time.sleep")
def test_wait_for_single_regex_pass(time_sleep_mock):
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9"
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
    assert w_cond.wait_for_regex("line1", timeout = 0.1, config = config)
    log_file.close()

@patch("time.sleep")
def test_wait_for_single_regex_fail(time_sleep_mock):
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9"
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
    assert not w_cond.wait_for_regex("line7", timeout = 0.1, config = config)
    log_file.close()

@patch("time.sleep")
def test_wait_for_single_regex_pass_in_tuple(time_sleep_mock):
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9"
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
    assert w_cond.wait_for_regex(("line1",), timeout = 0.1, config = config)
    log_file.close()

@patch("time.sleep")
def test_wait_for_single_regex_fail_in_tuple(time_sleep_mock):
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    date_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-4]:[0-6][0-9]:[0-6][0-9"
    time_sleep_mock.side_effect = lambda time: logging.debug(f"sleep {time}")
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    ]
    log_file = os_proxy.create_tmp_file("w", data = "".join(text))
    config = {"wait_for_regex.date_regex" : date_regex, "wait_for_regex.date_format" : date_format, "wait_for_regex.path" : log_file.name}
    assert not w_cond.wait_for_regex(("line7",), timeout = 0.1, config = config)
    log_file.close()
