__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import datetime
import os

from vatf.executor import log_snapshot, shell
from vatf.utils import utils
from vatf.utils import os_proxy
from vatf.utils import dlt

_written_lines_count = None
_generated_lines = []
from vatf.utils import debug
from vatf.executor import wait

_dlt_daemon = None
_dlt_project_path = "/tmp/dlt-project"
_lines_in_one_write = 10

def setup_function():
    from vatf import vatf_api
    global _written_lines_count
    _written_lines_count = 0
    vatf_api.set_api_type(vatf_api.API_TYPE.EXECUTOR)
    global _dlt_daemon, _dlt_project_path
    _dlt_daemon = dlt.DltDaemon(_dlt_project_path)
    _dlt_daemon.start()

def teardown_function():
    global _dlt_daemon
    _dlt_daemon.stop()
    log_snapshot.stop()

def sleep_until_lines_in_file(log_snapshot, count):
    import time
    while count > log_snapshot.get_lines_count():
        time.sleep(0.1)

def generate_line():
    global _written_lines_count
    now = datetime.datetime.now()
    s = f"{now} line_{_written_lines_count}"
    _written_lines_count = _written_lines_count + 1
    global _lines_in_one_write
    return s, 2, _lines_in_one_write

def test_wait_for_regex():
    timestamp_format = "%Y-%m-%d %H:%M:%S.%f"
    timestamp_regex = "^[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\} [0-2][0-9]:[0-6][0-9]:[0-6][0-9].[0-9][0-9][0-9]"
    _dlt_project_path = "/tmp/dlt-project"
    _dlt_rootfs = os.path.join(_dlt_project_path, "rootfs")
    _dlt_receive_path = os.path.join(_dlt_rootfs, "bin/dlt-receive")
    log_file = utils.get_temp_file()
    log_path = log_file.name
    print(log_file.name)
    writer = dlt.DltWriter(_dlt_project_path)
    writer_t = None
    lines_count = 30
    try:
        command1 = f"{_dlt_receive_path} -a 127.0.0.1 | grep 'LOG- TEST' > {{log_path}}"
        writer_t = writer.write_in_async_loop(pre_callback = generate_line)
        config = {"wait_for_regex.command" : command1, "wait_for_regex.date_regex" : timestamp_regex, "wait_for_regex.date_format" : timestamp_format, "wait_for_regex.is_file_ring_buffer" : False}
        assert wait.wait_for_regex(regex = "line_2", timeout = 8, pause = 0.5, config = config)
    except shell.StderrException as ex:
        print(f"Expected StderrException: {ex}")
    except Exception as ex:
        import sys
        print(ex, file=sys.stderr)
        assert False
    finally:
        writer.stop()
