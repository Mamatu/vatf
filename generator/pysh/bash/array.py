from pysh import core
from pysh.bash import scope

class Array(core.Command):
    def __init__(self, name):
        core.Command.__init__(self)
        self.name = name
        self.cmdStr("${{{}[@]}}".format(self.name))
    def set(self, code):
        """Creates and returns set/assign output of operation into this variable"""
        cmd = core.Command()
        if type(code) is not Array:
            cmd.cmdStr((self.name, "=( $(", code, ") )"))
        if type(code) is Array:
            cmd.cmdStr((self.name, "=", code))
        return cmd
    def init(self):
        cmd = core.Command()
        cmd.cmdStr((self.name, "=()"))
        return cmd
    def getValues(self):
        """Creates and returns get of this variable"""
        cmd = core.Command()
        cmd.cmdStr("${{{}[@]}}".format(self.name))
        return cmd
    def appendCmd(self, code):
        """Creates and returns set/assign output of operation into this variable"""
        cmd = core.Command()
        if type(code) is not Array:
            cmd.cmdStr((self.name, "+=( $(", code, ") )"))
        if type(code) is Array:
            cmd.cmdStr((self.name, "+=", code))
        return cmd
    def append(self, code):
        return self.appendCmd(code)
    def appendValue(self, code):
        """Creates and returns set/assign output of operation into this variable"""
        cmd = core.Command()
        if type(code) is not Array:
            cmd.cmdStr((self.name, "+=( ", code, " )"))
        if type(code) is Array:
            cmd.cmdStr((self.name, "+=", code))
        return cmd
    def iterate(self, code, idx):
        cmd = core.Command()
        cmd.cmdStr("for ")
        cmd.cmdStr(idx)
        cmd.cmdStr(" in ")
        cmd.cmdStr("\"${{{}[@]}}\"".format(self.name))
        cmd.cmdStr("; ")
        cmd.cmdStr("do")
        cmd.cmdNL()
        cmd.cmdStr(code)
        cmd.cmdNL()
        cmd.cmdStr("done")
        return cmd
    def iterate_over_idx(self, code, idx):
        cmd = core.Command()
        cmd.cmdStr("for ")
        cmd.cmdStr(idx)
        cmd.cmdStr(" in ")
        cmd.cmdStr("\"${{!{}[@]}}\"".format(self.name))
        cmd.cmdStr("; ")
        cmd.cmdStr("do")
        cmd.cmdNL()
        cmd.cmdStr(code)
        cmd.cmdNL()
        cmd.cmdStr("done")
        return cmd
    def get_idx(self, idx):
        cmd = core.Command()
        cmd.cmdStr(("${", self.name,"[", idx.get(), "]}"))
        return cmd
    def print(self):
        cmd = core.Command()
        cmd.cmdStr("printf '%s' ")
        cmd.cmdStr("\"")
        cmd.cmdStr(self.getValues())
        cmd.cmdStr("\"")
        return cmd
    def echo(self):
        cmd = core.Command()
        cmd.cmdStr("echo ")
        cmd.cmdStr("\"")
        cmd.cmdStr(self.getValues())
        cmd.cmdStr("\"")
        return cmd
