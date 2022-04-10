from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import logging
import textwrap
from generator import play

class PlayTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    class Ctx:
        def __init__(self):
            pass
        def getExistedAudioFilesPathes(self):
            return ["/tmp/"]
    @patch("vatf.generator.config")
    @patch("os.listdir")
    @patch("os.path.isfile")
    def test_play_random(self, os_path_isfile_mock, os_listdir_mock, vatf_generator_config):
        vatf_generator_config.return_value = PlayTests.Ctx()
        os_listdir_mock.return_value = ["sample_1.wav", "sample_2.wav"]
        os_path_isfile_mock.return_value = True
        audiofile = play.get_random_audio_files()
        flag = (audiofile == ["sample_1.wav"] or audiofile == ["sample_2.wav"])
        self.assertTrue(flag)
