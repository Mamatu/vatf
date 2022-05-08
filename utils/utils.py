import datetime
import os
import re
import subprocess

import logging

import inspect

DATE_REGEX = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

TIMESTAMP_REGEX = DATE_REGEX
TIMESTAMP_FORMAT = DATE_FORMAT

def count_lines_in_file(path):
    return int(subprocess.check_output(f"wc -l {path}").split()[0])

def name_and_args():
    caller = inspect.stack()[1][0]
    args, _, _, values = inspect.getargvalues(caller)
    return [(i, values[i]) for i in args]

def get_temp_filepath():
    import tempfile
    return tempfile.NamedTemporaryFile().name

def open_temp_filepath(flag = "w+"):
    path = get_temp_filepath()
    return open(path, flag)

def find_in_dir(dirpath, pattern, suffix = None):
    output = None
    try:
        ls = os.listdir(dirpath)
    except FileNotFoundError:
        output = []
    if output == None:
        if suffix:
            pattern = f"{pattern}.*{suffix}"
        pattern = re.compile(pattern)
        output = [entity for entity in ls if pattern.match(str(entity))]
    logging.debug(f"{find_in_dir.__name__}: {output}")
    return output

def parse_number_suffix(string):
    number_array = ""
    for c in reversed(string):
        if c.isdigit():
            number_array += c
        else:
            break
    output = -1
    if number_array != "":
        output = int(number_array[::-1])
    logging.debug(f"{parse_number_suffix.__name__}: {output}")
    return output

def get_counter(dirpath, pattern, suffix = None):
    def remove_suffix(m, suffix):
        if suffix != None:
            return m[:-len(suffix)-1]
        else:
            return m
    matched = find_in_dir(dirpath, pattern)
    matched = [remove_suffix(m, suffix) for m in matched]
    numbers = [parse_number_suffix(m) for m in matched]
    numbers.sort()
    i = -1
    if len(numbers) > 0:
        i = numbers[-1]
    logging.debug(f"{get_counter.__name__}: {i}")
    return i

import enum

class GrepEntry:
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
    def FromSplit(line, line_offset = 0):
        out = line.split(':', 1)
        return GrepEntry(out[0], out[1], line_offset)

def grep(filepath, regex, removeTmpFiles = True, maxCount = -1, fromLine = 1):
    if fromLine < 1:
        raise Exception(f"Invalid fromLine value {fromLine}")
    if maxCount < -1:
        raise Exception(f"Invalid value of maxCount {maxCount}. It should be > -1")
    lineNumber = True #hardcode
    def makeArgs(lineNumber, maxCount):
        n_arg = "-n" if lineNumber else ""
        m_arg = " -m {maxCount}" if maxCount > -1 else ""
        return f"{n_arg}{m_arg} -a"
    args = makeArgs(lineNumber, maxCount)
    command = f"grep {args} \"{regex}\""
    if fromLine > 1:
        command = f"sed -n '{fromLine},$p' {filepath} | {command}"
    else:
        command = f"{command} {filepath}"
    if command == None:
        raise Exception("Grep command was failed on initialization")
    logging.debug(f"{grep.__name__}: {command}")
    with open_temp_filepath() as fout, open_temp_filepath() as ferr:
        logging.debug(f"{grep.__name__}: fout {fout.name}")
        logging.debug(f"{grep.__name__}: ferr {ferr.name}")
        def readlines(f):
            lines = f.readlines()
            line_offset = 0 if fromLine < 1 else fromLine - 1
            if not lineNumber:
                lines = [GrepEntry(matched = l, line_offset = line_offset) for l in lines]
            else:
                lines = [GrepEntry.FromSplit(l, line_offset = line_offset) for l in lines]
            return lines
        def remove():
            if removeTmpFiles:
                os.remove(ferr.name)
                os.remove(fout.name)
        process = subprocess.Popen(command, shell=True, stdout=fout, stderr=ferr)
        process.wait()
        if os.path.getsize(ferr.name) > 0:
            ferr.seek(0)
            err = readlines(ferr)
            remove()
            raise Exception(err)
        fout.seek(0)
        out = readlines(fout)
        remove()
        return out

def grep_regex_in_line(filepath, grep_regex, match_regex, removeTmpFiles = True, maxCount = -1, fromLine = 1):
    """
    :filepath - filepath for greping
    :grep_regex - regex using to match line by grep
    :match_regex - regex to extract specific data from line
    :removeTmpFiles - remove tmp files when finished
    :maxCount - max count of matched, if it is -1 it will be infinity
    :fromLine - start searching from specific line
    """
    if fromLine < 1:
        raise Exception(f"Invalid fromLine value {fromLine}")
    logging.debug(f"{grep_regex_in_line.__name__}: {name_and_args()}")
    out = grep(filepath, grep_regex, removeTmpFiles, maxCount = maxCount, fromLine = fromLine)
    rec = re.compile(match_regex)
    matched_lines = []
    for o in out:
        matched = o.search_in_matched(rec)
        if matched:
            matched_lines.append(o)
    return matched_lines

def get_modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def convert_to_utc(date):
    local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    local_timezone_now = datetime.datetime.now(local_timezone)
    return date - datetime.timedelta(seconds=local_timezone_now.utcoffset().total_seconds())

def get_total_milliseconds(dt):
    return dt / datetime.timedelta(milliseconds=1)
