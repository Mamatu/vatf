from pysh.bash import bg, top, timer, utils, cond
from pysh import core
from pysh import shells
from pysh.bash.var import *

import os
thisFile = os.path.basename(__file__)
scriptName = "/tmp/{}.sh".format(thisFile)
print (scriptName)

core.setShell(shells.BashFile(scriptName))

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
core.shnl(("printf \"%s\" \"", var1.get(), "\""))

cond.IF_ELSE(var1.equal("\"2020/08/02 12:33:45.123654\""), "exit 0", "exit 1")()
