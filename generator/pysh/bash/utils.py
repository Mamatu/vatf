from pysh import core
from pysh.bash import grep, date, awk, config

def findDateInFileLineWithPattern(filepath, pattern, dateFormat = config.DateFormat):
    fif = grep.FindInFile(filepath)
    fif.contains(pattern, '-m 1')
    fif.contains(date.convertToSearchPattern(dateFormat), "-Eo")
    return fif

def findDateInTextLineWithPattern(text, pattern, dateFormat = config.DateFormat):
    fit = grep.FindInText(text)
    fit.contains(pattern, '-m 1')
    fit.contains(date.convertToSearchPattern(dateFormat), "-Eo")
    return fit

def toShellStr(string):
    string = string.replace("\n", "\\n")
    return string

def countPatternInDir(ddir, pattern):
    cmd = core.Command()
    cmd.cmdStr(("$(ls ", ddir, " | grep ", pattern," | wc -l)"))
    return cmd
