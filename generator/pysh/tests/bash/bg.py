from unittest import TestCase
import pytest

from pysh.bash.bg import *
from pysh import core, shells

class BGTests(TestCase):
    def test_bg_1(self):
        try:
            with core.Test():
                bg = BackgroundProcess("sleep 20", 9)
                bg.launch()
                bg.kill()
        except shells.CommExitCode as commExitCode:
            print (commExitCode)
            self.assertTrue(False)
