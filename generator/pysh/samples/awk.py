from pysh.bash import bg, top, timer, utils, cond, awk
from pysh import core
from pysh import shells
from pysh.bash.var import *
from pysh.bash.awk import *

import textwrap
import os

thisFile = os.path.basename(__file__)
scriptName = "/tmp/{}.sh".format(thisFile)
filepath = "/tmp/{}.txt".format(thisFile)
print (scriptName)

core.setShell(shells.BashFile(scriptName))

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
awk.getLine(True)
awk.setFilepath(filepath)
awk.untilFirstMatch(True)
awk.fromLine(0)
line1.setCmd(awk.get())()
cond.IF(line1.notequal("\"2\""), "exit 1")()
awk.fromLine(line1)
line2.setCmd(awk.get())()
cond.IF(line2.notequal("\"6\""), "exit 1")()
