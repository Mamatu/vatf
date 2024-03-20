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
import errno

import logging
import textwrap
import os

from vatf.utils import utils, os_proxy
from vatf.executor import mkdir
from vatf.utils import libsampling

TIMESTAMP_REGEX = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

def test_get_creation_date_empty():
    f = os_proxy.create_tmp_file("tw")
    p = f.name
    expectedDate = utils.get_modification_date(p)
    actualDate = libsampling.get_creation_date(p, timestamp_format = TIMESTAMP_FORMAT)
    assert expectedDate == actualDate
    f.close()

def test_get_creation_date_has_date():
    date_str = "2020-12-19 17:59:17.172"
    f = os_proxy.create_tmp_file("tw", data = date_str)
    p = f.name
    expectedDate = datetime.datetime.strptime(date_str, TIMESTAMP_FORMAT)
    actualDate = libsampling.get_creation_date(p, timestamp_format = TIMESTAMP_FORMAT)
    assert expectedDate == actualDate
    f.close()

def test_get_creation_date_is_binary():
    data = [0x98, 0xaf, 0xb7, 0x93, 0xbb, 0x03, 0xbf, 0x8e]
    f = os_proxy.create_tmp_file("bw", data = bytes(data))
    p = f.name
    expectedDate = utils.get_modification_date(p)
    actualDate = libsampling.get_creation_date(p, timestamp_format = TIMESTAMP_FORMAT)
    assert expectedDate == actualDate
    f.close()

def test_find_start_end_regexes():
    start_regex = "DialogUXStateAggregator:executeSetState:from=THINKING,to=SPEAKING,validTransition=true"
    end_regex = "DialogUXStateAggregator:executeSetState:from=SPEAKING,to=IDLE,validTransition=true"
    regexes = libsampling.find_start_end_regexes("executor/uts/data/sampling/test_log.txt", start_regex, end_regex, 0, -1, timestamp_regex = TIMESTAMP_REGEX)
    assert "2021-12-22 18:32:58.850" == regexes[0][0].matched[0]
    assert "2021-12-22 18:33:02.292" == regexes[0][1].matched[0]
    assert "2021-12-22 18:33:14.189" == regexes[1][0].matched[0]
    assert "2021-12-22 18:33:19.309" == regexes[1][1].matched[0]
    logging.debug(f"Found regexes[0]: {regexes[0][0]}, {regexes[0][1]}")
    logging.debug(f"Found regexes[1]: {regexes[1][0]}, {regexes[1][1]}")

def test_extract_samples():
    recording_start_date = libsampling.get_recording_start_date("executor/uts/data/sampling/test_audio.pcm", "executor/uts/data/sampling/test_audio.pcm.date", timestamp_format = TIMESTAMP_FORMAT)
    assert datetime.datetime.strptime("2021-12-22 18:32:54.932014", TIMESTAMP_FORMAT) == recording_start_date
    start_regex = "DialogUXStateAggregator:executeSetState:from=THINKING,to=SPEAKING,validTransition=true"
    end_regex = "DialogUXStateAggregator:executeSetState:from=SPEAKING,to=IDLE,validTransition=true"
    regexes = libsampling.find_start_end_regexes("executor/uts/data/sampling/test_log.txt", start_regex, end_regex, 0, -1, timestamp_regex = TIMESTAMP_REGEX)
    samples = libsampling.extract_samples(recording_start_date, regexes, "executor/uts/data/sampling/test_audio.wav", "/tmp/", sample_format = "wav", timestamp_format = TIMESTAMP_FORMAT)
    import hashlib
    assert (len(samples) == 2)
    def checksum(path):
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    sample = samples[0]
    assert checksum(sample) == checksum("executor/uts/data/sampling/sample_0.wav")
    sample = samples[1]
    assert checksum(sample) == checksum("executor/uts/data/sampling/sample_1.wav")
