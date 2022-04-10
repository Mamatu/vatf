from unittest import TestCase
import pytest

from pysh.bash import utils, cond
from pysh.bash.var import *
from pysh.bash.awk import *
from pysh import core, shells
from pysh.tests import test

import textwrap

def uuid():
    import uuid
    return str(uuid.uuid4())[:8]

class AwkTests(TestCase):
    def test_find_date_in_line(self):
        filepath = f"/tmp/pysh.awk.test.txt"
        scriptpath = f"/tmp/pysh.awk.sh"
        import os
        try:
            os.remove(filepath)
            os.remove(scriptpath)
        except FileNotFoundError:
            pass
        def body():
            line1 = Var("line1")
            line2 = Var("line2")
            text = """
            2020/08/02 12:33:44.123654 patternNotToFound
            2020/08/02 12:33:45.123654 patternToFound
            2020/08/02 12:33:46.123654 patternNotToFound
            2020/08/02 12:33:47.123654 patternNotToFound
            2020/08/02 12:33:48.123654 patternNotToFound
            2020/08/02 12:33:49.123654 patternToFound
            """
            file = open(filepath, "w")
            file.write(textwrap.dedent(text).strip())
            file.close()

            awk = Awk()
            awk.setPattern("patternToFound")
            awk.setFilepath(filepath)
            awk.untilFirstMatch(True)
            awk.fromLine(0)
            awk.getLine(True)
            line1.setCmd(awk.get())()
            cond.IF(line1.notequal("\"2\""), "exit 1")()
            awk.fromLine(line1)
            line2.setCmd(awk.get())()
            cond.IF(line2.notequal("\"6\""), "exit 1")()
        test.inShell(body, 0, lambda: shells.BashFile(scriptpath))
