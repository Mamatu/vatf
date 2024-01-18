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
from vatf.utils import utils
import tempfile
import pytest

def teardown_module():
    config_handler.reset_configs()

def test_load_config():
    data_temp_dir = tempfile.TemporaryDirectory()
    data_temp_dirpath = data_temp_dir.name
    #data_temp_dirpath = "/tmp/data"
    config = f'{{"tools" : {{"pathes" : ["{data_temp_dirpath}", "{data_temp_dirpath}/test_1"]}}}}'
    config_temp_file = utils.get_temp_file(suffix = ".json")
    with open(config_temp_file.name, "w") as f:
        f.write(config)
    config_handler.init_configs([f"{config_temp_file.name}"])
    libtools.create_tools_dir_form_config()
    assert ['tools', 'test_1'] == os.listdir(data_temp_dirpath)
    assert ".templates" in os.listdir(os.path.join(data_temp_dirpath, "tools"))
    assert ".templates" in os.listdir(os.path.join(data_temp_dirpath, "test_1/tools"))
    assert "template.convert_all_pcm_to_ogg.sh" in os.listdir(os.path.join(data_temp_dirpath, "tools/.templates"))
    assert "template.convert_all_pcm_to_ogg.sh" in os.listdir(os.path.join(data_temp_dirpath, "test_1/tools/.templates"))

