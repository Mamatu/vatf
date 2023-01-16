__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import inspect

_debug_enabled = True

def enable_debug(flag):
    global _debug_enabled
    _debug_enabled = flag

def print_info(extra_str = "", debug_mode = False):
    global _debug_enabled
    _print_debug = False
    if debug_mode:
        _print_debug = True
    else:
        _print_debug = _debug_enabled
    if _print_debug:
        _str = f"{inspect.stack()[2][1]} {inspect.stack()[2][2]} {inspect.stack()[2][3]} {extra_str}"
        print(_str)

def pi(extra_str = "", debug_mode = False):
    print_info(extra_str, debug_mode)
