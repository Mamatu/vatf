from unittest import TestCase
import pytest

from pysh import core, shells
from pysh.bash import func, top, sleep

from timeit import default_timer as timer

class FuncsTests(TestCase):
    def test_funcs_1(self):
        sleepTime = 0.1
        def body():
            cmd = core.Command()
            cmd.cmdStr(top.top())
            cmd.cmdNL()
            cmd.cmdStr(sleep.sleep(sleepTime))
            return cmd
        start = timer()
        with core.Test():
            foo = func.declare("foo", body())()
            func.call(foo)()
        end = timer()
        assert (end - start) > sleepTime
    def test_funcs_2(self):
        sleepTime = 0.4
        def body():
            cmd = core.Command()
            cmd.cmdStr(top.top())
            cmd.cmdNL()
            cmd.cmdStr(sleep.sleep(sleepTime))
            return cmd
        start = timer()
        with core.Test():
            foo = func.declare("foo", body())()
            func.call(foo)()
        end = timer()
        assert (end - start) > sleepTime
