from pysh import core
from pysh.bash import scope, sleep

def IF(condition, body):
    cmd = core.Command()
    cmd.cmdStr("if [[ ")
    cmd.cmdStr(condition)
    cmd.cmdStr(" ]]")
    cmd.cmdNL()
    cmd.cmdStr("then")
    cmd.cmdNL()
    cmd.cmdStr(body)
    cmd.cmdNL()
    cmd.cmdStr("fi")
    return cmd

def IF_ELSE(condition, true, false):
    cmd = core.Command()
    cmd.cmdStr("if [[ ")
    cmd.cmdStr(condition)
    cmd.cmdStr(" ]]")
    cmd.cmdNL()
    cmd.cmdStr("then")
    cmd.cmdNL()
    cmd.cmdStr(true)
    cmd.cmdNL()
    cmd.cmdStr("else")
    cmd.cmdNL()
    cmd.cmdStr(false)
    cmd.cmdNL()
    cmd.cmdStr("fi")
    return cmd
