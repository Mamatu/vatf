__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import datetime
import logging
import os

from vatf.utils import gstreamer, ac

class GstreamerTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    @staticmethod
    def _get_temp_filename():
        import tempfile
        return tempfile.NamedTemporaryFile().name
    def test_merge_pipelines(self):
        self.assertEqual(gstreamer.merge_pipelines([["a","b"], "c", "d"], ["1", "2", ["3", "4"]]), "a b ! c ! d ! 1 ! 2 ! 3 4")
    def test_make_json_info(self):
        recording_path = "/tmp/recording.pcm"
        audio_config = ac.AudioConfig(ac.Format.s16le, 1, 16000)
        expected = '{"info": [{"recording_path": "/tmp/recording.pcm", "creation_time": "2021-12-22 15:11:51.110758", "samples_rate": 16000, "format": "s16le", "channels": 1}]}'
        temp_filename = GstreamerTests._get_temp_filename()
        gstreamer.make_json_info(recording_path, temp_filename, audio_config, "%Y-%m-%d %H:%M:%S.%f", datetime.datetime.strptime("2021-12-22 15:11:51.110758", "%Y-%m-%d %H:%M:%S.%f"))
        actual = ""
        with open(temp_filename, "tr") as f:
            actual = f.read()
        self.assertEqual(expected, actual)
        os.remove(temp_filename)
