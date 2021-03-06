from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import datetime
import errno

import logging
import textwrap
import os

from vatf.utils import utils, os_proxy
from vatf.executor import mkdir, sampling

def test_get_creation_date_empty():
    p = os_proxy.create_file("tw")
    expectedDate = utils.get_modification_date(p)
    actualDate = sampling.get_creation_date(p)
    assert expectedDate == actualDate
    os_proxy.remove_file(p)

def test_get_creation_date_has_date():
    date_str = "2020-12-19 17:59:17.172"
    p = os_proxy.create_file("tw", data = date_str)
    expectedDate = datetime.datetime.strptime(date_str, sampling.DATE_FORMAT)
    actualDate = sampling.get_creation_date(p)
    assert expectedDate == actualDate
    os_proxy.remove_file(p)

def test_get_creation_date_is_binary():
    data = [0x98, 0xaf, 0xb7, 0x93, 0xbb, 0x03, 0xbf, 0x8e]
    p = os_proxy.create_file("bw", data = bytes(data))
    expectedDate = utils.get_modification_date(p)
    actualDate = sampling.get_creation_date(p)
    assert expectedDate == actualDate
    os_proxy.remove_file(p)

def test_find_start_end_regexes():
    start_regex = "DialogUXStateAggregator:executeSetState:from=THINKING,to=SPEAKING,validTransition=true"
    end_regex = "DialogUXStateAggregator:executeSetState:from=SPEAKING,to=IDLE,validTransition=true"
    regexes = sampling.find_start_end_regexes("executor/uts/data/sampling/test_log.txt", start_regex, end_regex, 0, -1)
    assert "2021-12-22 18:32:58.850" == regexes[0][0].matched[0]
    assert "2021-12-22 18:33:02.292" == regexes[0][1].matched[0]
    assert "2021-12-22 18:33:14.189" == regexes[1][0].matched[0]
    assert "2021-12-22 18:33:19.309" == regexes[1][1].matched[0]
    logging.debug(f"Found regexes[0]: {regexes[0][0]}, {regexes[0][1]}")
    logging.debug(f"Found regexes[1]: {regexes[1][0]}, {regexes[1][1]}")

def test_extract_samples():
    recording_start_date = sampling.get_recording_start_date("executor/uts/data/sampling/test_audio.pcm", "executor/uts/data/sampling/test_audio.pcm.date")
    assert datetime.datetime.strptime("2021-12-22 18:32:54.932014", sampling.DATE_FORMAT) == recording_start_date
    start_regex = "DialogUXStateAggregator:executeSetState:from=THINKING,to=SPEAKING,validTransition=true"
    end_regex = "DialogUXStateAggregator:executeSetState:from=SPEAKING,to=IDLE,validTransition=true"
    regexes = sampling.find_start_end_regexes("executor/uts/data/sampling/test_log.txt", start_regex, end_regex, 0, -1)
    samples = sampling.extract_samples(recording_start_date, regexes, "executor/uts/data/sampling/test_audio.wav", "/tmp/", sample_format = "wav")
    import hashlib
    assert (len(samples) == 2)
    def checksum(path):
        with open(path, 'rb') as f:
            hashlib.md5(f.read()).hexdigest()
    sample = samples[0]
    assert checksum(sample) == checksum("executor/uts/data/sampling/sample_0.wav")
    sample = samples[1]
    assert checksum(sample) == checksum("executor/uts/data/sampling/sample_1.wav")
