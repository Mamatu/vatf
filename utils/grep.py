__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import logging
from vatf.utils.pylibcommons import libgrep

def grep(filepath, regex, **kwargs):
    return libgrep.grep(filepath, regex, **kwargs)

def grep_in_text(txt, regex, **kwargs):
    return libgrep.grep_in_text(txt, regex, **kwargs)

def grep_regex_in_line(filepath, grep_regex, match_regex, **kwargs):
    return libgrep.grep_regex_in_line(filepath, grep_regex, match_regex, **kwargs)
