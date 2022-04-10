from pysh import core

def top():
    cmd = core.Command()
    cmd.cmdStr("top -b -n1")
    return cmd
