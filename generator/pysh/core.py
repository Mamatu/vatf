from pysh import shells
import traceback

import logging, sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()
logger.disabled = True

def parseArgs():
    import sys, re
    def parse_args():
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("--log", help = "Enable logging", action="store_true")
        args, unknown = parser.parse_known_args()
        return args
    if re.search('pytest', sys.argv[0]):
        return None
    else:
        return parse_args()

args = parseArgs()
if args:
    if args.log:
        logger.disabled = False

class _ShellProxy:
    newLine = ["\n", "\r"]
    def __init__(self, sh, nl = False):
        self.sh = sh
        self.nl = nl
        self.pre_tmp = ""
        self.buffer = ""
    def __callsh(self, command):
        if command == "\n" or command == '\r' or command == "":
            self.set_pre("")
        self.sh("{}{}".format(self.pre_tmp, command))
        self.set_pre("")
    def set_pre(self, c):
        self.pre_tmp = c
    def __call__(self, command = ""):
        def recCall(command):
            if type(command) is list:
                for c in command:
                    recCall(c)
            elif type(command) is str:
                self.__callsh("{}{}".format(command, "\n" if self.nl else ""))
        recCall(command)

shellsStack = []

__shell = shells.Empty()
sh = _ShellProxy(__shell)
shnl = _ShellProxy(__shell, True)

class Command:
    newLine = "\n"
    def __init__(self):
        self.__code = []
    def _newLine(self):
        self.__code.append(Command.newLine)
    def _nl(self):
        self._newLine()
    def cmdNL(self):
        self._nl()
    def cmdStr(self, command):
        """Process command and to code"""
        self.__code.append(command)
        logging.debug("cmdStr: isCommand = %d type = %s", isinstance(command, Command), type(Command))
    def cmdStrNL(self, command):
        self.cmdStr(command)
        self.cmdNL()
    def cmdCopy(self, command):
        import copy
        """Copy command object and add to code"""
        self.__code.append(copy.deepcopy(command))
        logging.debug("cmdCopy: %s", str(self.__code[-1]))
    def cmdRef(self, command):
        """Add command ref into code"""
        self.__code.append(command)
        logging.debug("cmdRef: %s", str(self.__code[-1]))
    def process(self):
        logging.debug("process")
        if logger.disabled == False and logging.DEBUG >= logging.root.level:
            traceback.print_stack()
        logging.debug("Processing command: %d %s", len(self.__code), str(self.__code));
        for element in self.__code:
            if type(element) is tuple or type(element) is list:
                for e in element:
                    Command._processElm(e)
            else:
                Command._processElm(element)
    def __call__(self):
        global shnl, sh
        logging.debug(f"Calling command <{self.__code}> in shell <{sh}, {shnl}>")
        self.process()
        shnl()
    def __str__(self):
        return str(self.__code)
    def _processElm(command):
        global sh, shnl
        logging.debug("Processing elm <%s>", command)
        if command != None:
            if isinstance(command, Command):
                command.process()
            elif callable(command):
                command()
            elif type(command) is str:
                sh(command)
            elif type(command) is int:
                sh(str(command))
            elif type(command) is tuple or type(command) is list:
                for c in command:
                    Command._processElm(c)
            else:
                raise Exception("Not supported command of type: {}".format(type(command)))
        logging.debug(f"Processed elm <{command}> in shell <{sh}, {shnl}>")

def setShell(shell):
    logging.debug(f"{setShell.__name__} : {shell}")
    pushShell(shell)

def pushLineShell(shell):
    global sh, shnl
    shellsStack.append((sh, shnl))
    shell = getShell()
    sh = _ShellProxy(shell)
    shnl = _ShellProxy(shell)

def pushShell(shell):
    global sh, shnl, shellsStack
    shellsStack.append((sh, shnl))
    sh = _ShellProxy(shell)
    shnl = _ShellProxy(shell, True)

def popShell():
    global sh, shnl, shellsStack
    sh, shnl = shellsStack.pop()

def getShell():
    global sh
    return sh.sh

class Test:
    def __init__(self, Shell = shells.RuntimeShell):
        self.__shell = Shell()
    def __enter__(self):
        pushShell(self.__shell)
    def __exit__(self, type, value, tb):
        popShell()
        self.__shell.exec()
