from pysh import core
from pysh.bash import scope

_funcs = []

def declare(name, body):
    class FuncCommand(core.Command):
        def __init__(self, name):
            core.Command.__init__(self)
            self.name = name
        def __call__(self):
            core.Command.__call__(self)
            return self.name
    cmd = FuncCommand(name)
    cmd.cmdStr("function {} {{".format(name))
    cmd.cmdNL()
    cmd.cmdStr(body)
    cmd.cmdNL()
    cmd.cmdStr("}")
    cmd.cmdNL()
    _funcs.append(name)
    return cmd

def call(name, *args):
    cmd = core.Command()
    if name != None and name != "":
        if name not in _funcs:
            raise Exception("Function {} was not created by 'declare' function".format(name))
        cmd.cmdStr("{} {}".format(name, " ".join(args)))
    return cmd
