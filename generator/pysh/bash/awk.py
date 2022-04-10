from pysh import core
from pysh.bash.var import *

class Awk:
    def __init__(self):
        core.Command.__init__(self)
        self.pattern = ""
        self.inputDelimiter = " "
        self.outputDelimiter = " "
        self._columnsToPrint = []
        self._printLine = True
        self.startLine = None
        self._untilFirstMatch = False
        self.filepath = ""
    def setPattern(self, pattern):
        """Pattern to find by awk. It is not mandatory"""
        self.pattern = pattern
    def setInputDelimiter(self, delimiter):
        """Inpout delimiter which will be used to seprate columns in file/text"""
        self.inputDelimiter = delimiter
    def setOutputDelimiter(self, delimiter):
        """Output delimiter which will be used to print output"""
        self.outputDelimiter = delimiter
    def setFilepath(self, filepath):
        """Path to processed file. It is mandatory."""
        self.filepath = filepath
    def fromLine(self, line):
        self.startLine = line
    def untilFirstMatch(self, b):
        """If true, awk will stop after matching the frist occurence"""
        self._untilFirstMatch = b
    def getColumns(self, column):
        """Specifies which columns will be printed as output"""
        if type(column) is list:
            for c in column:
                self.printColumns(c)
        if type(column) is int:
            self._columnsToPrint.append(column)
        if type(column) is str:
            self._columnsToPrint.append(column)
    def getLine(self, v):
        self._printLine = v
    def get(self):
        """Gets command of awk"""
        if not self.filepath:
            raise Exception("Filepath cannot be empty")
        cmd = core.Command()
        def printSection():
            sections = []
            printSection = ""
            if self._printLine:
                printSection = f"NR"
            for c in self._columnsToPrint:
                printSection = "{}{}".format(printSection, "${}".format(c) if c else "")
            printSection = f"print {printSection}"
            sections.append(printSection)
            if self._untilFirstMatch:
                sections.append("exit;")
            section = ";".join(sections)
            cmd.cmdStr(f"{{{section}}}")
        def condSection():
            parts = []
            startLine = None
            if self.startLine != None or type(self.startLine) is int:
                cmd.cmdStr("NR>")
                cmd.cmdStr(self.startLine)
            if self.pattern:
                if self.startLine != None or type(self.startLine) is int:
                    cmd.cmdStr("&&")
                cmd.cmdStr("/{}/".format(self.pattern))
        def beginSection():
            cmd.cmdStr("{}".format("BEGIN {{{fs_s};{ofs_s}}}".format(fs_s = f"FS=\"{self.inputDelimiter}\"", ofs_s = f"OFS=\"{self.outputDelimiter}\"")))
        cmd.cmdStr("awk ")
        cmd.cmdStr("'")
        beginSection()
        condSection()
        printSection()
        cmd.cmdStr("'")
        cmd.cmdStr(" ")
        cmd.cmdStr(self.filepath)
        return cmd
