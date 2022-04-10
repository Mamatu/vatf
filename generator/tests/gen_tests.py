from unittest import TestCase
from unittest.mock import Mock

import logging
import textwrap
from vatf.generator import gen_tests

class GenTestsTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    def test_make_pycall(self):
        self.assertEqual("foo()", gen_tests.make_pycall("foo"))
        self.assertEqual("foo('a')", gen_tests.make_pycall("foo", "a"))
        self.assertEqual("foo(a = 'a')", gen_tests.make_pycall("foo", a = "a"))
        self.assertEqual("foo('a', a = 'a')", gen_tests.make_pycall("foo", "a", a = "a"))
        self.assertEqual("foo('a', 1, a = 'a', b = 2)", gen_tests.make_pycall("foo", "a", 1, a = "a", b = 2))
        self.assertEqual("foo('a', 1, ('c', 'd'), a = 'a', b = 2)", gen_tests.make_pycall("foo", "a", 1, ("c", "d"), a = "a", b = 2))
        self.assertEqual("foo('a', 1, ('c', 'd'), a = 'a', b = 2, c = {'e': 9, 'f': 10})", gen_tests.make_pycall("foo", "a", 1, ("c", "d"), a = "a", b = 2, c = {"e": 9, "f": 10}))
    #def test_searched_audio_files_pathes_as_str(self):
    #    config = cfg.Config("generator/tests/config.json")
    #    test = Mock()
    #    get_tests.CreateTest(config, "/tmp/suite", "test", test)
    #    pathes = get_tests.Get().getAudioFilesPathes("example.mp3")
    #    self.assertTrue(isinstance(pathes, list))
    #    self.assertEqual(config.abs_audio_files_path_in_test, "/tmp/suite/test/assets/audio_files");
    #    self.assertEqual(pathes, ["/tmp/assets/audio_files/example.mp3"])
    #    test.assert_called_once()
    #def test_searched_audio_files_pathes_as_list(self):
    #    config = cfg.Config("generator/tests/config.json")
    #    test = Mock()
    #    get_tests.CreateTest(config, "/tmp/suite", "test", test)
    #    pathes = get_tests.Get().getAudioFilesPathes("example.mp3")
    #    self.assertTrue(isinstance(pathes, list))
    #    self.assertEqual(config.abs_audio_files_path_in_test, "/tmp/suite/test/assets/audio_files");
    #    self.assertEqual(pathes, ["/tmp/assets/audio_files/example.mp3"])
    #    test.assert_called_once()
    #def test_searched_audio_files_pathes_as_list_two_pathes(self):
    #    config = cfg.Config("generator/tests/config.json")
    #    test = Mock()
    #    get_tests.CreateTest(config, "/tmp/suite", "test", test)
    #    pathes = get_tests.Get().getAudioFilesPathes("example.mp3")
    #    self.assertTrue(isinstance(pathes, list))
    #    self.assertEqual(config.abs_audio_files_path_in_test, "/tmp/suite/test/assets/audio_files");
    #    self.assertEqual(pathes, ["/tmp/assets/audio_files/example.mp3"])
    #    test.assert_called_once()
