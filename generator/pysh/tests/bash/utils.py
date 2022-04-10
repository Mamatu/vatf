from unittest import TestCase
import pytest

from pysh.bash import utils
from pysh.bash.var import *
from pysh import core, shells
from pysh.tests import test

class UtilsTests(TestCase):
    def test_find_date_in_line(self):
        filepath = "/tmp/pysh.utils.sh"
        def body():
            var1 = Var("date1")
            text = """
            2020/08/02 12:33:44.123654 patternNotToFound
            2020/08/02 12:33:45.123654 patternToFound
            2020/08/02 12:33:46.123654 patternNotToFound
            2020/08/02 12:33:47.123654 patternNotToFound
            2020/08/02 12:33:48.123654 patternNotToFound
            2020/08/02 12:33:49.123654 patternToFound
            """
            var1.set(utils.findDateInTextLineWithPattern(utils.toShellStr(text), "patternToFound"))()
            core.shnl(("echo ", var1.get()))
        test.inShell(body, 0, lambda: shells.BashFile(filepath))
