__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import errno

import logging
import textwrap
import os

from vatf.executor import player, mkdir

class PopenMock:
    def __init__(self):
        pass
    def wait(self):
        pass

class PlayTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    def setUp(self):
        from vatf import vatf_api
        vatf_api.set_api_type(vatf_api.API_TYPE.EXECUTOR)
        logging.getLogger().setLevel(logging.INFO)
    @patch("subprocess.Popen")
    def test_play_audio(self, subprocess_popen_mock):
        subprocess_popen_mock.return_value = PopenMock()
        self.assertTrue(player)
        self.assertTrue(player.play_audio)
        player.play_audio(path = "utterance.mp3")
