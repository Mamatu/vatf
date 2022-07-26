import logging
from unittest import TestCase
from unittest.mock import Mock, call, ANY
from unittest.mock import patch

import textwrap
from vatf.generator import player
from vatf.utils import os_proxy

class PlayerTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    def setUp(self):
        logging.getLogger().setLevel(logging.INFO)
    @patch("vatf.utils.os_proxy.exists")
    @patch("vatf.utils.os_proxy.isfile")
    @patch("vatf.utils.os_proxy.listdir")
    def test_play_random(self, listdir_mock, exists_mock, isfile_mock):
        listdir_mock.return_value = ["sample_1.wav", "sample_2.wav"]
        isfile_mock.return_value = True
        exists_mock.return_value = True
        audiofile = player.get_random_audio_files("/tmp/assets/audio_files")
        flag = (audiofile == ["sample_1.wav"] or audiofile == ["sample_2.wav"])
        self.assertTrue(flag)
    #@patch("vatf.utils.config.get_pathes_to_audio_files_in_system")
    #@patch("vatf.utils.os_proxy.exists")
    #@patch("vatf.utils.os_proxy.isfile")
    #@patch("vatf.utils.os_proxy.listdir")
    #@patch("vatf.generator.player.play_audio")
    #def test_play_random_1(self, play_audio, listdir_mock, exists_mock, isfile_mock, get_pathes_to_audio_files_in_system_mock):
    #    get_pathes_to_audio_files_in_system_mock.return_value = ["/tmp/"]
    #    listdir_mock.return_value = ["sample_1.wav", "sample_2.wav"]
    #    isfile_mock.return_value = True
    #    exists_mock.return_value = True
    #    player.play_random_audio(audiofiles = ["sample_1.wav"], count = 1)
    #    play_audio.assert_has_calls([call("sample_1.wav")])
