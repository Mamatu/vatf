from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import errno

import logging
import textwrap
import mkdir
import os

import play

class PopenMock:
    def __init__(self):
        pass
    def wait(self):
        pass

class PlayTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    @patch("subprocess.Popen")
    def test_play_audio(self, subprocess_popen_mock):
        subprocess_popen_mock.return_value = PopenMock()
        play.PlayAudio("utterance.mp3")
