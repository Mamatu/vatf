from pysh.bash import bg, top, timer
from pysh import core
from pysh import shells

import os
thisFile = os.path.basename(__file__)
scriptName = "/tmp/{}.sh".format(thisFile)
print (scriptName)

core.setShell(shells.BashFile(scriptName))

v = timer.start()
bg = bg.BackgroundProcess("sleep 20", 9)
bg.launch()
top.top()
bg.kill()
top.top()
v = timer.measure(v)
core.sh(("echo ", v))
