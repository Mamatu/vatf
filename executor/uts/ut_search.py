from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import datetime
import errno

import logging
import textwrap
import os

from vatf.utils import utils, os_proxy, config_handler
from vatf.executor import search

def teardown_module():
    config_handler.reset_configs()

def test_search_find_one_regex():
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    "2022-01-29 20:54:56.568 line7\n"
    ]
    path = os_proxy.create_file("w", data = "".join(text))
    output = search.find("line5", filepath = path)
    assert len(output) == 1
    assert output[0][0] == 5
    assert output[0][1] == "2022-01-29 20:54:55.570 line5"
    os_proxy.remove(path)

def test_search_find_one_regex_from_config():
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    "2022-01-29 20:54:56.568 line7\n"
    ]
    config_handler.init_configs(["executor/uts/data/search/config.json"])
    path = os_proxy.create_file("w", data = "".join(text), path = "/tmp/tmp_search_test_config.log")
    assert "/tmp/tmp_search_test_config.log" == config_handler.handle(["va_log.path"])["va_log.path"]
    output = search.find("line5")
    assert len(output) == 1
    assert output[0][0] == 5
    assert output[0][1] == "2022-01-29 20:54:55.570 line5"
    os_proxy.remove(path)

def test_search_find_one_regex_only_match():
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    "2022-01-29 20:54:56.568 line7\n"
    ]
    path = os_proxy.create_file("w", data = "".join(text))
    output = search.find("line5", filepath = path, only_match = True)
    assert len(output) == 1
    assert output[0][0] == 5
    assert output[0][1] == "line5"
    os_proxy.remove(path)

def test_search_find_one_regex_only_match_from_config():
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    "2022-01-29 20:54:56.568 line7\n"
    ]
    config_handler.init_configs(["executor/uts/data/search/config.json"])
    path = os_proxy.create_file("w", data = "".join(text), path = "/tmp/tmp_search_test_config.log")
    assert "/tmp/tmp_search_test_config.log" == config_handler.handle(["va_log.path"])["va_log.path"]
    output = search.find("line5", only_match = True)
    assert len(output) == 1
    assert output[0][0] == 5
    assert output[0][1] == "line5"
    os_proxy.remove(path)

def test_search_find_regex_only_match():
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    "2022-01-29 20:54:56.568 line7\n"
    ]
    path = os_proxy.create_file("w", data = "".join(text))
    output = search.find("line[5,6,7]", filepath = path, only_match = True)
    assert len(output) == 3
    assert output[0][0] == 5
    assert output[0][1] == "line5"
    assert output[1][0] == 6
    assert output[1][1] == "line6"
    assert output[2][0] == 7
    assert output[2][1] == "line7"
    os_proxy.remove(path)

def test_search_find_regex_only_match_path_from_config():
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    "2022-01-29 20:54:56.568 line7\n"
    ]
    config_handler.init_configs(["executor/uts/data/search/config.json"])
    path = os_proxy.create_file("w", data = "".join(text), path = "/tmp/tmp_search_test_config.log")
    assert "/tmp/tmp_search_test_config.log" == config_handler.handle(["va_log.path"])["va_log.path"]
    output = search.find("line[5,6,7]", filepath = None, only_match = True)
    assert len(output) == 3
    assert output[0][0] == 5
    assert output[0][1] == "line5"
    assert output[1][0] == 6
    assert output[1][1] == "line6"
    assert output[2][0] == 7
    assert output[2][1] == "line7"
    os_proxy.remove(path)

def test_search_contains():
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    "2022-01-29 20:54:56.568 line7\n"
    ]
    path = os_proxy.create_file("w", data = "".join(text))
    assert False == search.contains("line8", filepath = path)
    assert True == search.contains("line7", filepath = path)
    assert False == search.contains("line0", filepath = path)
    os_proxy.remove(path)

def test_search_contains_path_from_config():
    text = [
    "2022-01-29 20:54:55.567 line1\n",
    "2022-01-29 20:54:55.567 line2\n",
    "2022-01-29 20:54:55.568 line3\n",
    "2022-01-29 20:54:55.569 line4\n",
    "2022-01-29 20:54:55.570 line5\n",
    "2022-01-29 20:54:55.600 line6\n",
    "2022-01-29 20:54:56.568 line7\n"
    ]
    config_handler.init_configs(["executor/uts/data/search/config.json"])
    path = os_proxy.create_file("w", data = "".join(text), path = "/tmp/tmp_search_test_config.log")
    assert "/tmp/tmp_search_test_config.log" == config_handler.handle(["va_log.path"])["va_log.path"]
    assert False == search.contains("line8")
    assert True == search.contains("line7")
    assert False == search.contains("line0")
    os_proxy.remove(path)
