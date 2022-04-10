from pysh import core
from pysh.bash import scope

class _Grep:
    def __grep(self, pattern, args = ""):
        core.sh(' | grep {} "{}"'.format(args, pattern))
    def __init__(self, readCmd = None):
        if readCmd != None:
            core.sh('{}'.format(readCmd))
    def match(self, pattern, args = ""):
        self.__grep("^{}$".format(pattern), args)
        return self
    def contain(self, pattern, args = ""):
        self.__grep("{}".format(pattern), args)
        return self
    def endStdout(self, code):
        if code:
            core.sh.set_pre(" | ")
            scope.handle(code)
        self.end()
    def endBool(self, codeOnTrue, codeOnFalse):
        if codeOnTrue:
            core.sh.set_pre(" && ")
            scope.handle(codeOnTrue)
        if codeOnFalse:
            core.sh.set_pre(" || ")
            scope.handle(codeOnFalse)
        self.end()
    def end(self):
        core.shnl("")

class _GrepText(_Grep):
    def __init__(self, text):
        _Grep.__init__(self, 'printf "{}"'.format(text))

class _GrepFile(_Grep):
    def __init__(self, filepath):
        _Grep.__init__(self, 'cat {}'.format(filepath))

def inText(text):
    return _GrepText(text)

def inFile(filepath):
    return _GrepFile(filepath)

class GrepInText(core.Command):
    def __init__(self, text):
        core.Command.__init__(self)
        self.cmdStr("printf \"{}\"".format(text))
    def matches(self, pattern, args = ""):
        self.cmdStr(" | grep {} \"^{}$\"".format(args, pattern))
    def contains(self, pattern, args = ""):
        self.cmdStr(" | grep {} \"{}\"".format(args, pattern))
    def endBool(self, codeOnTrue, codeOnFalse):
        self.cmdStr(codeOnTrue, prefixIfProcessed = " && ")
        self.cmdStr(codeOnFalse, prefixIfProcessed = " || ")

class GrepInFile(core.Command):
    def __init__(self, filepath, reverse = False):
        core.Command.__init__(self)
        if reverse == False:
            self.cmdStr("cat {}".format(text))
        else:
            self.cmdStr("tac {}".format(text))
    def matches(self, pattern, args = ""):
        self.cmdStr(" | grep {} \"^{}$\"".format(args, pattern))
    def contains(self, pattern, args = ""):
        self.cmdStr(" | grep {} \"{}\"".format(args, pattern))
    def last():
        self.cmdStr(" | tail -n");
    def endBool(self, codeOnTrue, codeOnFalse):
        self.cmdStr(codeOnTrue, prefixIfProcessed = " && ")
        self.cmdStr(codeOnFalse, prefixIfProcessed = " || ")


class FindInText(GrepInText):
    def __init__(self, text):
        GrepInText.__init__(self, text)

class FindInFile(GrepInFile):
    def __init__(self, filepath):
        GrepInFile.__init__(self, filepath)

class FindInFileReverse(GrepInFile):
    def __init__(self, filepath):
        GrepInFile.__init__(self, filepath, True)
