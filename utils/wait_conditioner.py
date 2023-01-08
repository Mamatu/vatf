__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from vatf.utils.wait_types import Label
from vatf.utils.wait_types import RegexOperator

def _get_operators(regex):
    def regex_index(_regex, _ro):
        try:
            return _regex.index(_ro)
        except ValueError:
            return -1
    occurences = [regex_index(regex, ro) for ro in RegexOperator]
    no_regex_operators_count = len([o for o in occurences if o == -1])
    if no_regex_operators_count != len(occurences) - 1 and no_regex_operators_count != len(occurences):
        raise Exception(f"Only one logical operator is expected {regex}")
    if no_regex_operators_count == len(occurences):
        return RegexOperator.EXISTS
    occurences.sort(reverse = True)
    index = occurences.pop(0)
    return regex[index]

def _remove_operator(regex, ro):
    idx = regex.index(ro)
    if idx == -1:
        raise Exception(f"No {ro} operator in handle {ro} data")
    del regex[idx]
    return regex

def _make_outputs(regex, filepath, ro, callback, **kwargs):
    outputs = []
    label_local_keys = []
    _regex = []
    from vatf.utils.kw_utils import handle_kwargs
    labels = handle_kwargs("labels", default_output = None, is_required = False, **kwargs)
    for r in regex:
        if isinstance(r, bool):
            outputs.append(r)
            _regex.append(r)
        elif isinstance(r, Label):
            if labels is None:
                raise Exception(f"Labels output dicts must be provided to kwargs if Label are used")
            label_local_keys.append(r.label)
        elif isinstance(r, str):
            from vatf.executor import search
            outputs.extend(search.find(filepath = filepath, regex = r))
            _regex.append(r)
        elif isinstance(r, RegexOperator):
            pass
        else:
            raise Exception(f"Not supported type in {r} in {regex}")
    out = callback(outputs, _regex)
    for llk in label_local_keys:
        if llk in labels:
            if labels[llk] and not out:
                raise Exception(f"FATAL: Incorrect sequence of outputs for label {llk}. The previous status was True and current output is False what is invalid!")
        labels[llk] = out
    return out

def _handle_exists(regex, filepath, **kwargs):
    def callback(outputs, regex):
        if len(regex) != 1:
            raise Exception(f"{RegexOperator.EXISTS} hadnles only single operator")
        if len(outputs) == 0:
            return False
        return outputs[0] is not None
    return _make_outputs(regex, filepath, RegexOperator.EXISTS, callback, **kwargs)

def _handle_and(regex, filepath, **kwargs):
    def callback(outputs, regex):
        if len(outputs) == len(regex):
            status = all(outputs)
            if status: return True
        return False
    return _make_outputs(regex, filepath, RegexOperator.AND, callback, **kwargs)

def _handle_or(regex, filepath, **kwargs):
    def callback(outputs, regex):
        for o in outputs:
            if o: return True
        return False
    return _make_outputs(regex, filepath, RegexOperator.OR, callback, **kwargs)

def _handle_in_order_line(regex, filepath, **kwargs):
    def callback(outputs, regex):
        _out = []
        for o in outputs:
            if isinstance(o, bool):
                _out.append(o)
            else:
                _out.append(o is not None)
        if all(_out):
            lines = [o.line_number if o else o for o in outputs]
            return lines == sorted(lines)
        return False
    return _make_outputs(regex, filepath, RegexOperator.IN_ORDER_LINE, callback, **kwargs)

def _handle_in_order_log_timestamp(regex, filepath, **kwargs):
    raise Exception("Not supported yet")
    if not "timestamp_regex" in kwargs:
        raise Exception("RegexOperator.IN_ORDER_LOG_TIMESTAMP requires timestamp_regex from config")
    timestamp_regex = kwargs['timestamp_regex']
    def callback(outputs, regex):
        _out = [o is not None for o in outputs]
        if all(_out):
            lines = [o.line_number if o else o for o in outputs]
            return lines == sorted(lines)
        return False
    return _make_outputs(regex, filepath, RegexOperator.IN_ORDER_LOG_TIMESTAMP, callback, **kwargs)

def _handle_in_order_real_timestamp(regex, filepath, **kwargs):
    raise Exception("Not supported yet")
    def callback(outputs, regex):
        _out = [o is not None for o in outputs]
        if all(_out):
            lines = [o.line_number if o else o for o in outputs]
            return lines == sorted(lines)
        return False
    return _make_outputs(regex, filepath, RegexOperator.IN_ORDER_REAL_TIMESTAMP, callback, **kwargs)

def _handle_regex_operator(regex, ro, filepath, **kwargs):
    _handlers = {
            RegexOperator.EXISTS : _handle_exists,
            RegexOperator.AND : _handle_and,
            RegexOperator.OR : _handle_or,
            RegexOperator.IN_ORDER_LINE : _handle_in_order_line,
            RegexOperator.IN_ORDER_REAL_TIMESTAMP : _handle_in_order_real_timestamp}
    if ro in _handlers.keys():
        return _handlers[ro](regex, filepath, **kwargs)
    else:
        raise Exception(f"Not supported regex operator: {ro}")

def _is_array(r):
    return isinstance(r, list) or isinstance(r, tuple)

def _handle_single_regex(regex, filepath):
    from vatf.executor import search
    out = search.find(filepath = filepath, regex = regex)
    return out

def _handle_multiple_regexes(regex, filepath, **kwargs):
    outputs = []
    for r in regex:
        if _is_array(r):
            out = _handle_multiple_regexes(r, filepath, **kwargs)
            assert isinstance(out, bool)
            idx = regex.index(r)
            regex[idx] = out
    ro = _get_operators(regex)
    return _handle_regex_operator(regex, ro, filepath, **kwargs)

def _wait_loop(regex, timeout, pause, filepath, start_point, **kwargs):
    from vatf.utils import config_handler, loop
    timestamp_regex = config_handler.get_var("wait_for_regex.date_regex", **kwargs)
    def handle():
        if _is_array(regex):
            import copy
            regex_copy = copy.deepcopy(regex)
            return _handle_multiple_regexes(regex_copy, filepath, timestamp_regex = timestamp_regex, **kwargs)
        else:
            return _handle_single_regex(regex, filepath)
    return loop.wait_until_true(handle, pause = pause, timeout = timeout)

def _wait_for_regex_command(regex, timeout = 30, pause = 0.5, **kwargs):
    import vatf.executor.lib_log_snapshot as log_snapshot_class
    log_snapshot = log_snapshot_class.make()
    from vatf.utils import utils
    temp_file = utils.get_temp_file()
    temp_filepath = temp_file.name
    try:
        wait_command_key = "wait_for_regex.command"
        from vatf.utils import config_handler
        command = config_handler.get_var(wait_command_key, **kwargs)
        command = command.format(log_path = temp_filepath)
        log_snapshot.start_cmd(log_path = temp_filepath, shell_cmd = command)
        import time
        start_point = time.time()
        return _wait_loop(regex, timeout, pause, temp_filepath, start_point, **kwargs)
    finally:
        log_snapshot.stop()
        temp_file.close()

def _wait_for_regex_path(regex, timeout = 30, pause = 0.5, **kwargs):
    import vatf.executor.lib_log_snapshot as log_snapshot_class
    wait_for_regex_path_key = "wait_for_regex.path"
    wait_for_regex_date_format_key = "wait_for_regex.date_format"
    wait_for_regex_date_regex_key = "wait_for_regex.date_regex"
    wait_path_vars_key = [wait_for_regex_path_key, wait_for_regex_date_format_key, wait_for_regex_date_regex_key]
    from vatf.utils import config_handler
    output = config_handler.get_vars(wait_path_vars_key, **kwargs)
    log_filepath = output[wait_for_regex_path_key]
    date_format = output[wait_for_regex_date_format_key]
    date_regex = output[wait_for_regex_date_regex_key]
    import time
    start_point = time.time()
    return _wait_loop(regex, timeout, pause, log_filepath, start_point, **kwargs)

def wait_for_regex(regex, timeout = 30, pause = 0.5, **kwargs):
    from vatf.utils import config_handler
    if config_handler.has_var("wait_for_regex.command", **kwargs):
        return _wait_for_regex_command(regex, timeout = timeout, pause = pause, **kwargs)
    else:
        return _wait_for_regex_path(regex, timeout = timeout, pause = pause, **kwargs)
