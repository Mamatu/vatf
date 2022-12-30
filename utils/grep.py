__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import logging

class GrepOutput:
    def __init__(self, line_number = None, matched = None, line_offset = 0):
        if line_number:
            try:
                self.line_number = int(line_number.rstrip())
                self.line_number = self.line_number + line_offset
            except Exception as ex:
                logging.error(f"{line_number} cannot be converted to int! ${ex}")
                raise ex
        self.matched = matched.rstrip()
    def __getitem__(self, idx):
        if idx == 0:
            return self.line_number
        if idx == 1:
            return self.matched
        raise IndexError
    def search_in_matched(self, rec):
        self.matched = rec.search(self.matched)
        return self.matched
    def __str__(self):
        return f"({self.line_number}, {self.matched})"
    @staticmethod
    def from_split(line, line_offset = 0):
        out = line.split(':', 1)
        return GrepOutput(out[0], out[1], line_offset)

def grep(filepath, regex, maxCount = -1, fromLine = 1, onlyMatch = False):
    from vatf.utils.utils import open_temp_file
    import subprocess, os
    if fromLine < 1:
        raise Exception(f"Invalid fromLine value {fromLine}")
    if maxCount < -1:
        raise Exception(f"Invalid value of maxCount {maxCount}. It should be > -1")
    lineNumber = True #hardcode
    def makeArgs(lineNumber, maxCount):
        o_arg = " -o" if onlyMatch else ""
        n_arg = " -n" if lineNumber else ""
        m_arg = " -m {maxCount}" if maxCount > -1 else ""
        return f"{o_arg}{n_arg}{m_arg} -a"
    args = makeArgs(lineNumber, maxCount)
    command = f"grep {args} \"{regex}\""
    if fromLine > 1:
        command = f"sed -n '{fromLine},$p' {filepath} | {command}"
    else:
        command = f"{command} {filepath}"
    if command == None:
        raise Exception("Grep command was failed on initialization")
    logging.debug(f"{grep.__name__}: {command}")
    with open_temp_file() as fout, open_temp_file() as ferr:
        logging.debug(f"{grep.__name__}: fout {fout.name}")
        logging.debug(f"{grep.__name__}: ferr {ferr.name}")
        def readlines(f):
            lines = f.readlines()
            line_offset = 0 if fromLine < 1 else fromLine - 1
            if not lineNumber:
                lines = [GrepOutput(matched = l, line_offset = line_offset) for l in lines]
            else:
                lines = [GrepOutput.from_split(l, line_offset = line_offset) for l in lines]
            return lines
        process = subprocess.Popen(command, shell=True, stdout=fout, stderr=ferr)
        process.wait()
        if os.path.getsize(ferr.name) > 0:
            ferr.seek(0)
            err = readlines(ferr)
            remove()
            raise Exception(err)
        fout.seek(0)
        out = readlines(fout)
        return out

def grep_in_text(txt, regex, maxCount = -1, fromLine = 1, onlyMatch = False):
    from vatf.utils import os_proxy
    try:
        file = create_tmp_file("w+", data = txt)
        return grep(file, regex, maxCount, fromLine, onlyMatch)
    finally:
        file.close()

def grep_regex_in_line(filepath, grep_regex, match_regex, maxCount = -1, fromLine = 1):
    """
    :filepath - filepath for greping
    :grep_regex - regex using to match line by grep
    :match_regex - regex to extract specific data from line
    :maxCount - max count of matched, if it is -1 it will be infinity
    :fromLine - start searching from specific line
    """
    from vatf.utils.utils import open_temp_file, name_and_args
    import re
    if fromLine < 1:
        raise Exception(f"Invalid fromLine value {fromLine}")
    logging.debug(f"{grep_regex_in_line.__name__}: {name_and_args()}")
    out = grep(filepath, grep_regex, maxCount = maxCount, fromLine = fromLine)
    rec = re.compile(match_regex)
    matched_lines = []
    for o in out:
        matched = o.search_in_matched(rec)
        if matched:
            matched_lines.append(o)
    return matched_lines
