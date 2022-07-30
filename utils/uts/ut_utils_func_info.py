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
    assert "foo (('x', 'a'), ('b', 'b'))" in captured.out

def test_print_func_info_2(capsys):
    def foo():
        utils.print_func_info()
    foo()
    captured = capsys.readouterr()
    assert "foo ()" in captured.out
