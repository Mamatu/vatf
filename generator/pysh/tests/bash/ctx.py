from unittest import TestCase
import pytest

from pysh import core, shells

class CtxTests(TestCase):
    def test_bash_exit0(self):
        with core.Test(lambda: shells.BashFile("/tmp/test_exit_0.sh")):
            core.shnl("exit 0")
    def test_bash_exit1(self):
        commExitCode = None
        try:
            with core.Test(lambda: shells.BashFile("/tmp/test_exit_1.sh")):
                core.shnl("exit 1")
        except shells.CommExitCode as cec:
            commExitCode = cec
        assert commExitCode != None
        assert commExitCode.exitCode == 1
    def test_bash_exit2(self):
        commExitCode = None
        try:
            with core.Test(lambda: shells.BashFile("/tmp/test_exit_2.sh")):
                core.shnl("exit 2")
        except shells.CommExitCode as cec:
            commExitCode = cec
        assert commExitCode != None
        assert commExitCode.exitCode == 2
    def test_bash_exit3_in_test_exit_2(self):
        commExitCode = None
        try:
            with core.Test(lambda: shells.BashFile("/tmp/test_exit_2.sh")):
                core.shnl("exit 3")
        except shells.CommExitCode as cec:
            commExitCode = cec
        assert commExitCode != None
        assert commExitCode.exitCode == 3
