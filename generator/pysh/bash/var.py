from pysh import core
from pysh.bash import scope

class Var(core.Command):
    def __init__(self, name):
        core.Command.__init__(self)
        self.name = name
        self.cmdStr("${}".format(self.name))
    def set(self, v):
        return self.setCmd(v)
    def setCmd(self, code):
        """Creates and returns set/assign output of operation into this variable"""
        cmd = core.Command()
        if type(code) is not Var:
            cmd.cmdStr((self.name, "=$(", code, ")"))
        if type(code) is Var:
            cmd.cmdStr((self.name, "=", code))
        return cmd
    def setValue(self, value):
        """Creates and returns set/assign value into this variable"""
        cmd = core.Command()
        cmd.cmdStr((self.name, "="))
        cmd.cmdStr(value)
        return cmd
    def get(self):
        """Creates and returns get of this variable"""
        cmd = core.Command()
        cmd.cmdStr("${}".format(self.name))
        return cmd
    def equal(self, var):
        cmd = core.Command()
        cmd.cmdStr((self.get(), " == "))
        if isinstance(var, Var):
            cmd.cmdStr(var.get())
        else:
            cmd.cmdStr(var)
        return cmd
    def notequal(self, var):
        cmd = core.Command()
        cmd.cmdStr((self.get(), " != "))
        if isinstance(var, Var):
            cmd.cmdStr(var.get())
        else:
            cmd.cmdStr(var)
        return cmd
    def handle(var):
        if type(var) is int:
            return str(var)
        if type(var) is Var:
            return "${}".format(var.getName())
