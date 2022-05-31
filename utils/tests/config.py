from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import datetime
import logging
import os

from vatf.utils import config, config_loader

class ConfigTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    def test_load_config_in_tests(self):
        c = config_loader.load("utils/tests/config.json")
        self.assertEqual(2, len(c.config.assets.audio.files))
        self.assertEqual("track1.wav", c.config.assets.audio.files[0].name)
        self.assertEqual(1, len(c.config.assets.audio.files[0].tags))
        self.assertEqual("track1", c.config.assets.audio.files[0].tags[0])
        self.assertEqual("track2.wav", c.config.assets.audio.files[1].name)
        self.assertEqual(1, len(c.config.assets.audio.files[1].tags))
        self.assertEqual("track2", c.config.assets.audio.files[1].tags[0])
        self.assertEqual("/tmp/session.log", c.config.va_log.path)
        self.assertEqual(datetime.timedelta(hours=-1), c.config.va_log.timedelta)
        self.assertEqual(1, len(c.config.utterance_from_va.regexes))
        self.assertEqual("start_utterance", c.config.utterance_from_va.regexes[0].begin)
        self.assertEqual("end_utterance", c.config.utterance_from_va.regexes[0].end)
        self.assertEqual(None, c.config.utterance_to_va)
    def test_convert_to_log_zone(self):
        config.load("utils/tests/config.json")
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        dt = datetime.datetime.strptime("2022-01-20 12:30:34.564879", date_format)
        dt = config.convert_to_log_zone(dt)
        self.assertEqual("2022-01-20 11:30:34.564879", dt.strftime(date_format))
        dt = config.convert_to_system_zone(dt)
        self.assertEqual("2022-01-20 12:30:34.564879", dt.strftime(date_format))
    def test_get_regexes_for_sampling(self):
        c = config_loader.load("utils/tests/config.json")
        regexes = c.config.utterance_from_va.regexes
        self.assertEqual(1, len(regexes))
        self.assertEqual(2, len(regexes[0]))
        self.assertEqual("start_utterance", regexes[0][0])
        self.assertEqual("end_utterance", regexes[0][1])
