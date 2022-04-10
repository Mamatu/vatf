from pysh import core
from pysh.bash import grep, config

_converts = {
    "%Y":["[0-9][0-9][0-9][0-9]"],
    "%m":["[0-1][0-9]"],
    "%d":["[0-2][0-9]", "3[0-1]"],
    "%H":["[0-1][0-9]","2[0-3]"],
    "%M":"[0-5][0-9]",
    "%S":"[0-5][0-9]",
    "%6N":"[0-9][0-9][0-9][0-9][0-9][0-9]"
}

def print(date_format = config.DateFormat):
    cmd = core.Command()
    cmd.cmdStr('echo $(date +"{}")'.format(date_format))
    return cmd

def get(date_format = config.DateFormat):
    cmd = core.Command()
    cmd.cmdStr('$(date +"{}")'.format(date_format))
    return cmd

def _date_format_into_search_pattern(df):
    grep = ""
    global _converts
    pattern = _converts[df]
    if type(pattern) is list:
        return "({})".format("|".join(pattern))
    if type(pattern) is str:
        return pattern

def convertToSearchPattern(dateFormat):
    grep = ""
    skip = []
    for idx in range(len(dateFormat)):
        c = dateFormat[idx]
        if idx in skip:
            continue
        if c == "%":
            number = None
            df = None
            try:
                number = int(dateFormat[idx+1])
            except ValueError:
                number = None
            nextIdx = idx + 1
            c = dateFormat[nextIdx]
            skip.append(idx + 1)
            if number != None:
                nextIdx = idx + 2
                c = dateFormat[nextIdx]
                skip.append(idx + 2)
            dformat = "%{}{}".format("" if number == None else number, c)
            grep = "{}{}".format(grep, _date_format_into_search_pattern(dformat))
        else:
            grep = "{}{}".format(grep, c)
    return grep
