from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import datetime
import errno

import logging
import textwrap
import mkdir
import os

import sampling
from vatf_utils import utils

class SamplingTests(TestCase):
    def __init__(self, arg):
        logging.basicConfig(level=logging.DEBUG)
        TestCase.__init__(self, arg)
    def create_file(self, mode, data = None):
        path = utils.get_temp_filepath()
        with open(path, mode) as f:
            if data:
                f.write(data)
        return path
    def remove_file(self, path):
        os.remove(path)
    def test_get_creation_date_empty(self):
        p = self.create_file("tw")
        expectedDate = utils.get_modification_date(p)
        actualDate = sampling.GetCreationDate(p)
        self.assertEqual(expectedDate, actualDate)
        self.remove_file(p)
    def test_get_creation_date_has_date(self):
        date_str = "2020-12-19 17:59:17.172"
        p = self.create_file("tw", data = date_str)
        expectedDate = datetime.datetime.strptime(date_str, sampling.DATE_FORMAT)
        actualDate = sampling.GetCreationDate(p)
        self.assertEqual(expectedDate, actualDate)
        self.remove_file(p)
    def test_get_creation_date_is_binary(self):
        data = [0x98, 0xaf, 0xb7, 0x93, 0xbb, 0x03, 0xbf, 0x8e]
        p = self.create_file("bw", data = bytes(data))
        expectedDate = utils.get_modification_date(p)
        actualDate = sampling.GetCreationDate(p)
        self.assertEqual(expectedDate, actualDate)
        self.remove_file(p)
    def test_find_start_end_regexes(self):
        start_regex = "DialogUXStateAggregator:executeSetState:from=THINKING,to=SPEAKING,validTransition=true"
        end_regex = "DialogUXStateAggregator:executeSetState:from=SPEAKING,to=IDLE,validTransition=true"
        regexes = sampling.FindStartEndRegexes("tests/data/sampling/test_log.txt", start_regex, end_regex, 0, -1)
        self.assertEqual("2021-12-22 18:32:58.850", regexes[0][0].matched[0])
        self.assertEqual("2021-12-22 18:33:02.292", regexes[0][1].matched[0])
        self.assertEqual("2021-12-22 18:33:14.189", regexes[1][0].matched[0])
        self.assertEqual("2021-12-22 18:33:19.309", regexes[1][1].matched[0])
        logging.debug(f"Found regexes[0]: {regexes[0][0]}, {regexes[0][1]}")
        logging.debug(f"Found regexes[1]: {regexes[1][0]}, {regexes[1][1]}")
    def test_extract_samples(self):
        recording_start_date = sampling.GetRecordingStartDate("tests/data/sampling/test_audio.pcm", "tests/data/sampling/test_audio.pcm.date")
        self.assertEqual(datetime.datetime.strptime("2021-12-22 18:32:54.932014", sampling.DATE_FORMAT), recording_start_date)
        start_regex = "DialogUXStateAggregator:executeSetState:from=THINKING,to=SPEAKING,validTransition=true"
        end_regex = "DialogUXStateAggregator:executeSetState:from=SPEAKING,to=IDLE,validTransition=true"
        regexes = sampling.FindStartEndRegexes("tests/data/sampling/test_log.txt", start_regex, end_regex, 0, -1)
        samples = sampling.ExtractSamples(recording_start_date, regexes, "tests/data/sampling/test_audio.wav", "/tmp/", sample_format = "wav")
        import hashlib
        self.assertTrue(len(samples) == 2)
        checksum = lambda path: hashlib.md5(open(path,'rb').read()).hexdigest()
        sample = samples[0]
        self.assertEqual(checksum(sample), checksum("tests/data/sampling/sample_0.wav"))
        sample = samples[1]
        self.assertEqual(checksum(sample), checksum("tests/data/sampling/sample_1.wav"))