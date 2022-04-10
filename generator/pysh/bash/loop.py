from pysh import core
from pysh.bash import scope, sleep

def while_loop(condition, body):
    cmd = core.Command()
    cmd.cmdStr("while [")
    cmd.cmdStr(condition)
    cmd.cmdStr("]")
    cmd.cmdNL()
    cmd.cmdStr("do")
    cmd.cmdNL()
    cmd.cmdStr(body)
    cmd.cmdNL()
    cmd.cmdStr("done")
    return cmd

def white_for(condition, time = 0.1):
    while_loop(condition, sleep.Sleep(time))
    return cmd
