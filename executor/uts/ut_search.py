from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import datetime
import errno

import logging
import textwrap
import os

from vatf.utils import utils, os_proxy
from vatf.executor import search

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
    output = search.find(path, "line5")
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
    output = search.find(path, "line5", onlyMatch = True)
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
    output = search.find(path, "line[5,6,7]", onlyMatch = True)
    assert len(output) == 3
    assert output[0][0] == 5
    assert output[0][1] == "line5"
    assert output[1][0] == 6
    assert output[1][1] == "line6"
    assert output[2][0] == 7
    assert output[2][1] == "line7"
    os_proxy.remove(path)
