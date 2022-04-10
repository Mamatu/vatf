from pysh.bash import bg, top, timer, utils, cond
from pysh import core
from pysh import shells
from pysh.bash.var import *
from pysh.bash.array import *

import os
thisFile = os.path.basename(__file__)
scriptName = "/tmp/{}.sh".format(thisFile)
print (scriptName)

core.setShell(shells.BashFile(scriptName))

array = Array("array")
array.append(1)
array.append(2)
array.append(3)

array.echo()
