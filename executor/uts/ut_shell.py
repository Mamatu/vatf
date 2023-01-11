__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from vatf.executor import shell
from vatf.utils import os_proxy

import psutil

def test_double_kill():
    try:
        p = shell.bg("sleep 100")
        shell.kill(p)
        shell.kill(p)
    except psutil.NoSuchProcess:
        assert False

def test_wc_in_fg():
    f = os_proxy.create_tmp_file(mode = "w", data = "line1\nline2\nline3\n")
    assert f"3 {f.name}" == shell.fg(f"wc -l {f.name}")
    f.close()
