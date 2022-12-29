import datetime
import os
import re
import subprocess

import logging

import inspect

def count_lines_in_file(path):
    wc_cmd = f"wc -l {path}"
    logging.debug(f"Launch {wc_cmd}")
    count = int(subprocess.check_output(wc_cmd).split()[0])
    logging.debug(f"{wc_cmd} returned {count}")
    return count

def touch(path):
    touch_cmd = f"touch {path} ; sync"
    logging.debug(touch_cmd)
    os.system(touch_cmd)

def name_and_args():
    caller = inspect.stack()[1][0]
    args, _, _, values = inspect.getargvalues(caller)
    return [(i, values[i]) for i in args]

def get_caller_args(caller):
    args, varargs, keywords, values = inspect.getargvalues(caller)
    output = [(i, values[i]) for i in args]
    if varargs: output.extend([(i) for i in values[varargs]])
    if keywords: output.extend([(k, v) for k, v in values[keywords].items()])
    return output

def get_func_info(level = 1):
    caller = inspect.stack()[level][0]
    function_name = inspect.stack()[level][3]
    args = get_caller_args(caller)
    for arg in args:
        if isinstance(arg, tuple):
            if len(arg) == 2:
                idx = args.index(arg)
                if isinstance(arg[1], str):
                    args[idx] = f"{arg[0]} = \'{arg[1]}\'"
                else:
                    args[idx] = f"{arg[0]} = {arg[1]}"
            elif len(arg) == 1:
                args[idx] = f"{arg[0]}"
            else:
                raise Exception("Not supported length of arg")
    args = map(lambda arg: str(arg), args)
    args = ", ".join(args)
    args = args.replace("[", "").replace("]", "").replace("\"", "")
    return f"{function_name} ({args})"

def print_func_info():
    print(get_func_info(level = 2))

def get_tmp_file(mode = "r+"):
    return get_temp_file(mode = mode)

def get_temp_file(mode = "r+"):
    import tempfile
    return tempfile.NamedTemporaryFile(mode = mode)

def open_temp_file(mode = "w+"):
    file = get_temp_file(mode = mode)
    return file

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

def grep(filepath, regex, removeTmpFiles = True, maxCount = -1, fromLine = 1, onlyMatch = False):
    from vatf.utils import grep
    return grep.grep(filepath, regex, removeTmpFiles, maxCount, fromLine, onlyMatch)

def grep_regex_in_line(filepath, grep_regex, match_regex, removeTmpFiles = True, maxCount = -1, fromLine = 1):
    from vatf.utils import grep
    return grep.grep_regex_in_line(filepath, grep_regex, match_regex, removeTmpFiles, maxCount, fromLine)

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

def get_modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def convert_to_utc(date):
    local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    local_timezone_now = datetime.datetime.now(local_timezone)
    return date - datetime.timedelta(seconds=local_timezone_now.utcoffset().total_seconds())

def get_total_milliseconds(dt):
    return dt / datetime.timedelta(milliseconds=1)
