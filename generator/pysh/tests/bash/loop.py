from unittest import TestCase
import pytest

from pysh.bash.loop import *
from pysh import core, shells

class LoopTests(TestCase):
    def test_while(self):
        try:
            with core.Test():
                def body():
                    core.shnl('echo "$x"')
                    core.shnl('x=$(( $x + 1 ))')
                core.shnl("x=1")
                while_loop("$x -le 5", body)
        except shells.CommExitCode as commExitCode:
            print (commExitCode)
            self.assertTrue(False)
