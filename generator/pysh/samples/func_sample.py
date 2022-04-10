from pysh.bash import bg, top, timer, func, date
from pysh import core
from pysh import shells

import os
thisFile = os.path.basename(__file__)
scriptName = "/tmp/{}.sh".format(thisFile)
print (scriptName)

core.setShell(shells.BashFile(scriptName))

foo = func.declare("foo", "top -b -n1")()
func.call(foo)()
