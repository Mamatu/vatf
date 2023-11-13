__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from vatf.utils.wait_types import Label
from vatf.utils.wait_types import RegexOperator

import os

def wait_for_regex(regex, timeout = 30, pause = 0.5, **kwargs):
    from vatf.utils import config_handler
    if config_handler.has_var("wait_for_regex.command", **kwargs):
        if config_handler.has_var("wait_for_regex.file_ring_buffer", **kwargs):
            return _wait_for_regex_command_file_ring_buffer(regex, timeout = timeout, pause = pause, **kwargs)
        else:
            return _wait_for_regex_command(regex, timeout = timeout, pause = pause, **kwargs)
    elif config_handler.has_var("wait_for_regex.path", **kwargs):
        return _wait_for_regex_path(regex, timeout = timeout, pause = pause, **kwargs)
    else:
        raise Exception("Lack of wait_for_regex attributes: command or path")

def _check_if_start_point_is_before_time(filepath, **kwargs):
    from vatf.utils.kw_utils import handle_kwargs
    start_point = handle_kwargs("start_point", default_output = None, is_required = True, **kwargs)
    with open(filepath, "r") as f:
        line = f.readline()
        from vatf.utils import grep
        from vatf.utils import config_handler
        from datetime import datetime
        config = config_handler.get_config(**kwargs)
        date_format = config.wait_for_regex.date_format
        date_regex = config.wait_for_regex.date_regex
        out = grep.grep_in_text(line, date_regex, only_match = True) 
        if len(out) != 1:
            raise Exception("Invalid outs from grep. It must be only one!")
        dt = datetime.strptime(out[0].matched, date_format)
        dt1 = datetime.strptime(start_point, date_format)
        return dt1 < dt

def _find_closest_date_greater_than_start_point(filepath, **kwargs):
    def strp(matched):
        import datetime
        return datetime.datetime.strptime(matched, date_format)
    from vatf.utils.kw_utils import handle_kwargs
    start_point = handle_kwargs("start_point", default_output = None, is_required = True, **kwargs)
    from vatf.utils import config_handler
    config = config_handler.get_config(**kwargs)
    date_format = config.wait_for_regex.date_format
    date_regex = config.wait_for_regex.date_regex
    from vatf.executor import search
    out = search.find(filepath = filepath, regex = date_regex, only_match = True)
    out = [o for o in out if strp(o.matched) > strp(start_point)]
    if len(out) == 0:
        return None
    return min(out, key = lambda x: abs(strp(x.matched) - strp(start_point)))

def _find(filepath, regex, **kwargs):
    from vatf.executor import search
    from vatf.utils.kw_utils import handle_kwargs
    start_point = handle_kwargs("start_point", default_output = None, is_required = False, **kwargs)
    line_number = 1
    if start_point:
        line = _find_closest_date_greater_than_start_point(filepath = filepath, **kwargs)
        if line is None:
            return []
        line_number = line.line_number
    return search.find(filepath = filepath, regex = regex, from_line = line_number, support_directory = True)

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
    labels_objects = handle_kwargs("labels_objects", default_output = None, is_required = True, **kwargs)
    for r in regex:
        if isinstance(r, bool):
            outputs.append(r)
            _regex.append(r)
        elif isinstance(r, Label):
            if r.label in labels_objects:
                label_object = labels_objects[r.label]
                if label_object is not r:
                    raise Exception(f"Two different Label objects have the same label {label_object} and {r}")
            if labels is None:
                raise Exception(f"Labels output dicts must be provided to kwargs if Label class is used")
            label_local_keys.append(r.label)
        elif isinstance(r, str):
            outputs.extend(_find(filepath = filepath, regex = r, **kwargs))
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
        if len(outputs) == 0:
            return False
        if len(regex) != 1:
            raise Exception(f"{RegexOperator.EXISTS} hadnles only single operator")
        if len(outputs) == 0:
            return False
        return outputs[0] is not None
    return _make_outputs(regex, filepath, RegexOperator.EXISTS, callback, **kwargs)

def _handle_and(regex, filepath, **kwargs):
    def callback(outputs, regex):
        if len(outputs) == 0:
            return False
        if len(outputs) == len(regex):
            status = all(outputs)
            if status: return True
        return False
    return _make_outputs(regex, filepath, RegexOperator.AND, callback, **kwargs)

def _handle_or(regex, filepath, **kwargs):
    def callback(outputs, regex):
        if len(outputs) == 0:
            return False
        for o in outputs:
            if o: return True
        return False
    return _make_outputs(regex, filepath, RegexOperator.OR, callback, **kwargs)

def _handle_in_order_line(regex, filepath, **kwargs):
    def callback(outputs, regex):
        outputs = outputs[:len(regex)]
        if len(outputs) == 0:
            return False
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

def _handle_single_regex(regex, filepath, **kwargs):
    out = _find(filepath = filepath, regex = regex, **kwargs)
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

def _wait_loop(regex, timeout, pause, filepath, **kwargs):
    from vatf.utils import config_handler, loop
    timestamp_regex = config_handler.get_var("wait_for_regex.date_regex", **kwargs)
    def handle():
        if _is_array(regex):
            import copy
            regex_copy = copy.deepcopy(regex)
            labels_objects = {}
            kwargs['labels_objects'] = labels_objects
            output = _handle_multiple_regexes(regex_copy, filepath, timestamp_regex = timestamp_regex, **kwargs)
            return output
        else:
            return _handle_single_regex(regex, filepath, **kwargs)
    return loop.wait_until_true(handle, pause = pause, timeout = timeout)

def _get_start_point(config, date_format_is_required = False):
    date_format = None
    timedelta = None
    start_point = None
    date_format_key = "wait_for_regex.date_format"
    timedelta_key = "wait_for_regex.timedelta"
    try:
        date_format = config[date_format_key]
    except:
        date_format = None
    try:
        timedelta = config[timedelta_key]
        from vatf.utils import config_common
        timedelta = config_common.convert_dict_to_timedelta(timedelta)
    except:
        timedelta = None
    if date_format:
        import datetime
        start_point = datetime.datetime.now()#.strftime(date_format)
    if start_point is not None and not date_format_is_required:
        return None
    elif start_point is None and date_format_is_required:
        raise Exception(f"{key} is required for this scenarion/mode")
    if start_point and timedelta:
        start_point = start_point + timedelta
    if start_point:
        start_point = start_point.strftime(date_format)
    return start_point

def _wait_for_regex_command(regex, timeout = 30, pause = 0.5, **kwargs):
    from vatf.utils import config_handler
    config = config_handler.get_config(**kwargs)
    timestamp_format = config.wait_for_regex.date_format
    timestamp_regex = config.wait_for_regex.date_regex
    from vatf.utils import lib_log_snapshot
    log_snapshot = lib_log_snapshot.make()
    from vatf.utils import utils
    temp_file = utils.get_temp_file()
    temp_filepath = temp_file.name
    try:
        from vatf.utils import config_handler
        config = config_handler.get_config(**kwargs)
        command = config.wait_for_regex.command
        command = command.format(log_path = temp_filepath)
        timestamps_kwargs = {"timestamp_format" : timestamp_format, "timestamp_regex" : timestamp_regex}
        log_snapshot.start_cmd(log_path = temp_filepath, shell_cmd = command, **timestamps_kwargs)
        start_point = _get_start_point(config)
        if start_point is not None:
            kwargs["start_point"] = start_point
        return _wait_loop(regex, timeout, pause, temp_filepath, **kwargs)
    finally:
        log_snapshot.stop()
        temp_file.close()

def _wait_for_regex_path(regex, timeout = 30, pause = 0.5, **kwargs):
    wait_for_regex_path_key = "wait_for_regex.path"
    wait_for_regex_date_format_key = "wait_for_regex.date_format"
    wait_for_regex_date_regex_key = "wait_for_regex.date_regex"
    wait_path_vars_key = [wait_for_regex_path_key, wait_for_regex_date_format_key, wait_for_regex_date_regex_key]
    from vatf.utils import config_handler
    config = config_handler.get_config(**kwargs)
    start_point = _get_start_point(config, date_format_is_required = True)
    if start_point is not None:
        kwargs["start_point"] = start_point
    log_filepath = config[wait_for_regex_path_key]
    date_format = config[wait_for_regex_date_format_key]
    date_regex = config[wait_for_regex_date_regex_key]
    return _wait_loop(regex, timeout, pause, log_filepath, **kwargs)

from vatf.utils import libcmdringbuffer

def _wait_for_regex_command_file_ring_buffer(regex, timeout = 30, pause = 0.5, **kwargs):
    from vatf.utils import config_handler
    config = config_handler.get_config(**kwargs)
    timestamp_format = config.wait_for_regex.date_format
    timestamp_regex = config.wait_for_regex.date_regex
    tmp_path = config.tmp.path
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    command = config.wait_for_regex.command
    chunks_dir_path = f"{tmp_path}/chunks"
    cmdringbuffer = libcmdringbuffer.make(command, f"{tmp_path}/fifo", chunks_dir_path, 1000, 5)
    temp_filepath = chunks_dir_path
    try:
        from vatf.utils import config_handler
        config = config_handler.get_config(**kwargs)
        command = config.wait_for_regex.command
        command = command.format(log_path = temp_filepath)
        timestamps_kwargs = {"timestamp_format" : timestamp_format, "timestamp_regex" : timestamp_regex}
        cmdringbuffer.start()
        start_point = _get_start_point(config)
        if start_point is not None:
            kwargs["start_point"] = start_point
        return _wait_loop(regex, timeout, pause, temp_filepath, **kwargs)
    finally:
        cmdringbuffer.stop()
