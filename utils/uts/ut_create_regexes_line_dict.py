__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import pytest
import logging
from unittest.mock import patch
from vatf.utils import os_proxy
from vatf.utils import wait_conditioner

from contextlib import contextmanager
from unittest.mock import patch

import datetime

# Source: https://stackoverflow.com/a/46919967
@contextmanager
def mocked_now(now):
    class MockedDatetime(datetime.datetime):
        @classmethod
        def now(cls):
            return now
    with patch("datetime.datetime", MockedDatetime):
        yield

def test_create_regexes_line_dict():
    from vatf.utils.pylibcommons import libgrep
    #grepOutput1 = libgrep.GrepOutput("2640", "2024/02/09 16:33:43.724963   33793601 106 XXXX XXXX XXXX xxx XXXX X X [[XXX: 11111]processActionFinished::lambda:448: Foo::processActionFinished(actions::Action*, bool)::<lambda()> Action finished successfully: PromptPlay { It is <time><time> 23:24</time></time>. }]", 0, "../xxxs/data/test/session_2024_02_09_16_33_32/xxx/session.xxx")
    grepOutput1 = libgrep.GrepOutput("2640", "2024/02/09 16:33:43.724963   33793601 106 XXXX XXXX XXXX xxx XXXX X 0 [[XXX: 11111]processActionFinished::lambda:448: Foo::bar(actions::Action*, bool)::<lambda()> Action finished successfully: PromptPlay { It is <time><time> 23:24</time></time>. }]", 0, "../xxxs/data/test/session_2024_02_09_16_33_32/xxx/session.xxx")
    grepOutput2 = libgrep.GrepOutput("2645", "2024/02/09 16:33:43.725016   33793607 111 XXXX XXXX XXXX xxx xxxx X 0 [[tID: 1529]Foo::setState:646: void Foo::foo(S) S { P } -> S { I }]", 0, "../xxxs/data/test/session_2024_02_09_16_33_32/xxx/session.xxx")
    grepOutput3 = libgrep.GrepOutput("2793", "2024/02/09 16:33:44.520690   33801555 179 XXXX XXXX XXXX xxx xxxx X 0 [[tID: 1529]Foo::setState:646: void Foo::foo(S) S { P } -> S { I }]", 0, "../xxxs/data/test/session_2024_02_09_16_33_32/xxx/session.xxx")
    outputs = [grepOutput1, grepOutput2, grepOutput3]
    #regexes = ['Action finished successfully: PromptPlay { It is.* }\\|Action finished successfully: PromptPlay { <time>.* }\\|Action finished successfully: PromptPlay { .*[0-9][0-9]:[0-9][0-9].* }', 'State { Prompting } -> State { Idle }']
    #regexes = ['Action finished successfully: PromptPlay { It is.* }\|Action finished successfully: PromptPlay { <time>.* }\|Action finished successfully: PromptPlay { .*[0-9][0-9]:[0-9][0-9].* }', 'State { Prompting } -> State { Idle }']
    regexes = ['Action finished successfully: PromptPlay { It is <time>.* }', 'S { P } -> S { I }']
    _dict = wait_conditioner._create_regexes_line_dict(outputs, regexes)
    print(_dict)

