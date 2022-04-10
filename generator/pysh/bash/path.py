from pysh import core
from pysh.bash import scope

def basename(p):
    cmd = core.Command()
    cmd.cmdStr(("basename ", p))
    return cmd

def dirname(p):
    cmd = core.Command()
    cmd.cmdStr(("dirname ", p))
    return cmd
