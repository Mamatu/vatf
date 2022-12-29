import enum
import time as t

class RegexOperators(enum.Enum):
    AND = 0,
    OR = 1,
    IN_ORDER = 3

def _make_outputs(regex, filepath, ro):
    import copy
    regex_copy = copy.copy(regex)
    idx = regex_copy.index(ro)
    if idx == -1:
        raise Exception(f"No {ro} operator in handle {ro} data")
    del regex_copy[idx]
    outputs = []
    for r in regex:
        if isinstance(r, bool):
            outputs.append(r)
        else:
            from vatf.executor import search
            outputs.append(search.find(filepath = filepath, regex = r))
    return outputs

def _handle_and(regex, filepath):
    outputs = _make_outputs(regex, filepath, RegexOperators.AND)
    return all(outputs)

def _handle_or(regex, filepath):
    outputs = _make_outputs(regex, filepath, RegexOperators.OR)
    for o in outputs:
        if o: return True
    return False

def _handle_in_order(regex, filepath):
    outputs = _make_outputs(regex, filepath, RegexOperators.IN_ORDER)
    for o in outputs:
        if o: return True
    return False

def _handle_single_regex(regex, filepath):
    from vatf.executor import search
    out = search.find(filepath = filepath, regex = regex)
    return out

def _is_array(r):
    return isinstance(r, list) or isinstance(r, tuple)

def _regex_operators_index(regex, filepath):
    import copy
    regex_copy = copy.copy(regex)
    regex_copy.reverse()
    for r in regex_copy:
        if _is_array(r):
            out = _regex_operators_index(r)
            assert isinstance(out, bool)
            idx = regex_copy.index(r)
            regex_copy[idx] = out
    regex_copy.reverse()
    occurences = [regex.index(ro) for ro in RegexOpearors]
    no_regex_operators_count = len([o for o in occurences if o == -1])
    if no_regex_operators_count != len(occurences) - 1:
        raise Exception("Only one logical operator is expected")
    occurences.sort(reverse = True)
    index = occurences.pop(0)
    ro = regex_copy[index]
    

def _handle_multiple_regexes(regex, filepath):
    pass

def _wait_loop(regex, timeout, pause, filepath, start_point):
    while True:
        out = None
        if _is_array(regex):
            out = _handle_multiple_regexes(regex, filepath)
        else:
            out = _handle_single_regex(regex, filepath)
        if out is not None and len(out) > 0:
            return True
        t.sleep(pause)
        end_point = t.time()
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
        start_point = t.time()
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
    start_point = t.time()
    return _wait_loop(regex, timeout, pause, log_filepath, start_point)

def wait_for_regex(regex, timeout = 30, pause = 0.5, **kwargs):
    from vatf.utils import config_handler
    if config_handler.has_var("wait_for_regex.command", **kwargs):
        return _wait_for_regex_command(regex, timeout = timeout, pause = pause, **kwargs)
    else:
        return _wait_for_regex_path(regex, timeout = timeout, pause = pause, **kwargs)
