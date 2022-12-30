__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import enum

class RegexOperator(enum.Enum):
    AND = 0,
    OR = 1,
    IN_ORDER = 2

def _get_operators(regex):
    def regex_index(_regex, _ro):
        try:
            return _regex.index(_ro)
        except ValueError:
            return -1
    occurences = [regex_index(regex, ro) for ro in RegexOperator]
    no_regex_operators_count = len([o for o in occurences if o == -1])
    if no_regex_operators_count != len(occurences) - 1:
        raise Exception("Only one logical operator is expected")
    occurences.sort(reverse = True)
    index = occurences.pop(0)
    return regex[index]

def _remove_operator(regex, ro):
    import copy
    regex_copy = copy.copy(regex)
    idx = regex_copy.index(ro)
    if idx == -1:
        raise Exception(f"No {ro} operator in handle {ro} data")
    del regex_copy[idx]
    return regex_copy

def _make_outputs(regex, filepath, ro):
    outputs = []
    for r in regex:
        if isinstance(r, bool):
            outputs.append(r)
        else:
            from vatf.executor import search
            outputs.extend(search.find(filepath = filepath, regex = r))
    return outputs

def _handle_and(regex, filepath):
    regex = _remove_operator(regex, RegexOperator.AND)
    outputs = _make_outputs(regex, filepath, RegexOperator.AND)
    if len(outputs) == len(regex):
        status = all(outputs)
        if status: return sorted(outputs, key = lambda o: o.line_number)[-1]
    return False

def _handle_or(regex, filepath):
    regex = _remove_operator(regex, RegexOperator.OR)
    outputs = _make_outputs(regex, filepath, RegexOperator.OR)
    for o in outputs:
        if o: return o
    return False

def _handle_in_order(regex, filepath):
    regex = _remove_operator(regex, RegexOperator.IN_ORDER)
    outputs = _make_outputs(regex, filepath, RegexOperator.IN_ORDER)
    _out = [o is not None for o in outputs]
    if all(_out):
        lines = [o.line_number if o else o for o in outputs]
        return lines == sorted(lines)
    return False

def _handle_regex_operator(regex, ro, filepath):
    if ro == RegexOperator.AND:
        return _handle_and(regex, filepath)
    elif ro == RegexOperator.OR:
        return _handle_or(regex, filepath)
    elif ro == RegexOperator.IN_ORDER:
        return _handle_in_order(regex, filepath)
    else:
        raise Exception(f"Not supported regex operator: {ro}")

def _is_array(r):
    return isinstance(r, list) or isinstance(r, tuple)

def _handle_single_regex(regex, filepath):
    from vatf.executor import search
    out = search.find(filepath = filepath, regex = regex)
    return out

def _handle_multiple_regexes(regex, filepath):
    import copy
    regex_copy = copy.copy(regex)
    regex_copy.reverse()
    for r in regex_copy:
        if _is_array(r):
            out = _handle_multiple_regexes(r, filepath)
            assert isinstance(out, bool)
            idx = regex_copy.index(r)
            regex_copy[idx] = out
    regex_copy.reverse()
    regex = regex_copy
    ro = _get_operators(regex)
    return _handle_regex_operator(regex, ro, filepath)

def _wait_loop(regex, timeout, pause, filepath, start_point):
    while True:
        status = False
        if _is_array(regex):
            status = _handle_multiple_regexes(regex, filepath)
        else:
            status = _handle_single_regex(regex, filepath)
        if status: return True
        import time
        time.sleep(pause)
        end_point = time.time()
        if (end_point - start_point) > timeout:
            print(f"timeout: {end_point} {start_point}")
            return False

def _wait_for_regex_command(regex, timeout = 30, pause = 0.5, **kwargs):
    import vatf.executor.log_snapshot_class as log_snapshot_class
    log_snapshot = log_snapshot_class.make()
    from vatf.utils import utils
    temp_file = utils.get_temp_file()
    temp_filepath = temp_file.name
    print(f"wait_for_regex -> {temp_filepath}")
    try:
        wait_command_key = "wait_for_regex.command"
        from vatf.utils import config_handler
        command = config_handler.get_var(wait_command_key, **kwargs)
        command = command.format(log_path = temp_filepath)
        log_snapshot.start(log_path = temp_filepath, shell_cmd = command)
        import time
        start_point = time.time()
        return _wait_loop(regex, timeout, pause, temp_filepath, start_point)
    finally:
        log_snapshot.stop()
        temp_file.close()

def _wait_for_regex_path(regex, timeout = 30, pause = 0.5, **kwargs):
    import vatf.executor.log_snapshot_class as log_snapshot_class
    wait_for_regex_path_key = "wait_for_regex.path"
    wait_for_regex_date_format_key = "wait_for_regex.date_format"
    wait_for_regex_date_regex_key = "wait_for_regex.date_regex"
    wait_path_vars_key = [wait_for_regex_path_key, wait_for_regex_date_format_key, wait_for_regex_date_regex_key]
    from vatf.utils import config_handler
    output = config_handler.get_vars(wait_path_vars_key, **kwargs)
    log_filepath = output[wait_for_regex_path_key]
    date_format = output[wait_for_regex_date_format_key]
    date_regex = output[wait_for_regex_date_regex_key]
    print(f"wait_for_regex -> {log_filepath}")
    import time
    start_point = time.time()
    return _wait_loop(regex, timeout, pause, log_filepath, start_point)

def wait_for_regex(regex, timeout = 30, pause = 0.5, **kwargs):
    from vatf.utils import config_handler
    if config_handler.has_var("wait_for_regex.command", **kwargs):
        return _wait_for_regex_command(regex, timeout = timeout, pause = pause, **kwargs)
    else:
        return _wait_for_regex_path(regex, timeout = timeout, pause = pause, **kwargs)
