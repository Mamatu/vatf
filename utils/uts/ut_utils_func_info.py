__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import datetime
import logging
import os

from vatf.utils import utils

import pytest

def test_print_func_info_1(capsys):
    def foo(x, b):
        utils.print_func_info()
    foo("a", "b")
    captured = capsys.readouterr()
    assert "foo (x = 'a', b = 'b')\n" == captured.out

def test_print_func_info_2(capsys):
    def foo():
        utils.print_func_info()
    foo()
    captured = capsys.readouterr()
    assert "foo ()\n" == captured.out

def test_print_func_info_3(capsys):
    def foo(alpha, **kwargs):
        utils.print_func_info()
    foo(alpha = 1, beta = 2, gamma = 3)
    captured = capsys.readouterr()
    assert "foo (alpha = 1, beta = 2, gamma = 3)\n" == captured.out

def test_print_func_info_4(capsys):
    def foo(alpha, *args, **kwargs):
        utils.print_func_info()
    foo(1, 4, 5,  beta = 2, gamma = 3)
    captured = capsys.readouterr()
    assert "foo (alpha = 1, 4, 5, beta = 2, gamma = 3)\n" == captured.out
