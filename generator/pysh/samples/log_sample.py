from pysh.bash import bg, top, timer, date, logging, sleep
from pysh.bash.loop import *
from pysh import core
from pysh import shells

import os
thisFile = os.path.basename(__file__)
scriptName = "/tmp/{}.sh".format(thisFile)
print (scriptName)

core.setShell(shells.BashFile(scriptName))

logging.logIntoFile("/tmp/{}.log".format(thisFile))

for idx in range(0, 6):
    date.print()
    sleep.sleep(0.2)
