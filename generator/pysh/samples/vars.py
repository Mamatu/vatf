from pysh.bash import bg, top, timer, utils, cond
from pysh import core
from pysh import shells
from pysh.bash.var import *

import os
thisFile = os.path.basename(__file__)
scriptName = "/tmp/{}.sh".format(thisFile)
print (scriptName)

core.setShell(shells.BashFile(scriptName))

var1 = Var("var1")
var1.setValue("2")()

var2 = Var("var2")
var2.setValue("1")()

cond.IF(var1.equal(var2), "exit 1")()
