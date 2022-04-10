from pysh import core
from pysh.bash.var import *
__counter = 0

class _TimerCommand(core.Command):
    def __init__(self, var):
        core.Command.__init__(self)
        self.var = var
    def __call__(self):
        core.Command.__call__(self)
        return self.var

def startCmd(var1 = None):
    global __counter
    __counter = __counter + 1
    var = Var("timer_start_{}".format(__counter))
    cmd = _TimerCommand(var)
    if var1 == None:
        cmd.cmdStr(var.setCmd("date +%s.%N"))
        cmd.cmdNL()
    else:
        cmd = var.setCmd(var1)
        cmd.cmdNL()
    return var, cmd

def start(var1 = None):
    var, cmd = startCmd(var1)
    cmd()
    return var

def measureCmd(var1):
    global __counter
    __counter = __counter + 1
    var = Var("timer_stop_{}".format(__counter))
    cmd = _TimerCommand(var)
    cmd.cmdStr(var.setCmd(("bc <<< \"$(date +%s.%N) - ", var1, "\"")))
    cmd.cmdNL()
    return var, cmd

def epsilonTime(var, var1, var2):
    return var.setCmd(("bc <<< \"$(date -d \"", var1 ,"\" +%s.%N) - $(date -d \"", var2, "\" +%s.%N)\""))

def endTimestamp(output, beginTimestamp, duration):
    return output.setCmd(("bc <<< \"", beginTimestamp, " + ", duration, "\""))

def measure(var1):
    var, cmd = measureCmd(var1)
    cmd()
    return var
