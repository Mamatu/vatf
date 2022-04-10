from unittest import TestCase
import pytest

from pysh.bash.grep import *
from pysh import core, shells
from pysh.tests import test

class GrepNewTests(TestCase):
    def test_match_exit0_1(self):
        fit = FindInText("test")
        fit.matches("test")
        test.inShell(fit, 0)
    def test_notmatch_exit1_2(self):
        fit = FindInText("test")
        fit.matches("test1")
        test.inShell(fit, 1)
    def test_contain_exit0_3(self):
        fit = FindInText("test1")
        fit.contains("test")
        test.inShell(fit, 0)
