from unittest import TestCase
import pytest

from pysh.bash.grep import *
from pysh import core, shells
from pysh.tests import test

class GrepTests(TestCase):
    def test_notmatch_exit1_1(self):
        test.inShell(lambda: inText("testa").match("test").endBool("exit 0", "exit 1"), 1)
    def test_notmatch_exit1_2(self):
        test.inShell(lambda: inText("textlongechotwo").match("echo").endBool("exit 0", "exit 1"), 1)
    def test_notmatch_exit1_3(self):
        test.inShell(lambda: inText("textlongechotwo").match("echo1").endBool("exit 0", "exit 1"), 1)
    def test_match_exit0_1(self):
        test.inShell(lambda: inText("test").match("test").endBool("exit 0", "exit 1"), 0)
    def test_match_exit0_2(self):
        test.inShell(lambda: inText("echo").match("ech[a-z]").endBool("exit 0", "exit 1"), 0)
    def test_match_exit0_3(self):
        test.inShell(lambda: inText("coredump").match("core.*").endBool("exit 0", "exit 1"), 0)
    def test_notcontain_exit1_1(self):
        test.inShell(lambda: inText("tesa").contain("test").endBool("exit 0", "exit 1"), 1)
    def test_notcontain_exit1_2(self):
        test.inShell(lambda: inText("textlongechtwo").contain("tst").endBool("exit 0", "exit 1"), 1)
    def test_notcontain_exit1_3(self):
        test.inShell(lambda: inText("textlongechtwo").contain("echo1").endBool("exit 0", "exit 1"), 1)
    def test_contain_exit0_1(self):
        test.inShell(lambda: inText("testa").contain("test").endBool("exit 0", "exit 1"), 0)
    def test_contain_exit0_2(self):
        test.inShell(lambda: inText("textlongecho12").contain("ech[a-z]").endBool("exit 0", "exit 1"), 0)
    def test_contain_exit0_3(self):
        test.inShell(lambda: inText("coredump loop cat").contain("core").endBool("exit 0", "exit 1"), 0)
