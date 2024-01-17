__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import datetime
import logging
import os

from vatf.utils import config_loader
from vatf.utils import config_handler
from vatf.utils import libtools

import pytest

def test_get():
    class Attr1:
        def __init__(self):
            self.attr2 = 3
    class Data:
        def __init__(self):
            self.attr1 = Attr1()
    data = Data()
    assert config_loader.get_attr(data, "attr1.attr2") == 3
    assert config_loader.get_attr(data, "attr1.attr3", False) == None

def teardown_module():
    config_handler.reset_configs()

def test_config_common_convert_dict_to_timedelta():
    from vatf.utils import config_common
    timedelta = config_common.convert_dict_to_timedelta({"hours" : -1})
    #assert timedelta.seconds == -3600

def test_load_config():
    config_handler.init_configs(["utils/uts/data/ut_libtools/config.json"])
    #assert c.tools.pathes == ["/tmp/data", "/tmp/data/test_1"]
    libtools.create_tools_dir_form_config()
