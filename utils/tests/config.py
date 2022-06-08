import datetime
import logging
import os

from vatf.utils import config

def test_load_config_raw():
    c = config.load_raw("utils/tests/config.json")
    assert c.assets.audio.path == "./assets/audio_files"
    assert c.va_log.path == "/tmp/session.log"
    assert c.va_log.command == "receive {ip}"
    assert c.va_log.timedelta.hours == -1
    assert c.va_log.date_format == "%Y-%m-%d %H:%M:%S.%f"
    assert c.va_log.date_regex == "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    assert c.utterance_from_va.regexes[0].begin == "start_utterance"
    assert c.utterance_from_va.regexes[0].end == "end_utterance"
    assert c.format[0].key ==  "ip"
    assert c.format[0].value ==  "172.0.0.1"

def test_load_config():
    c = config.load("utils/tests/config.json")
    assert c.assets.audio.path == "./assets/audio_files"
    assert c.va_log.path == "/tmp/session.log"
    assert c.va_log.command == "receive 172.0.0.1"
    assert c.va_log.timedelta.hours == -1
    assert c.va_log.date_format == "%Y-%m-%d %H:%M:%S.%f"
    assert c.va_log.date_regex == "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    assert c.utterance_from_va.regexes[0].begin == "start_utterance"
    assert c.utterance_from_va.regexes[0].end == "end_utterance"
    assert c.format[0].key ==  "ip"
    assert c.format[0].value ==  "172.0.0.1"

def test_load_config_with_custom_format():
    c = config.load("utils/tests/config_custom.json", {"session_name" : "session_1"})
    assert c.assets.audio.path == "./assets/audio_files"
    assert c.va_log.path == "/session_1/session.log"
    assert c.va_log.command == "receive 172.0.0.1"
    assert c.va_log.timedelta.hours == -1
    assert c.va_log.date_format == "%Y-%m-%d %H:%M:%S.%f"
    assert c.va_log.date_regex == "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    assert c.utterance_from_va.regexes[0].begin == "start_utterance"
    assert c.utterance_from_va.regexes[0].end == "end_utterance"
    assert c.format[0].key ==  "ip"
    assert c.format[0].value ==  "172.0.0.1"

def test_load_two_configs():
    c = config.load(["utils/tests/config1.json", "utils/tests/config2.json"])
    assert c.assets.audio.path == "./assets/audio_files"
    assert c.va_log.path == "/tmp/session.log"
    assert c.va_log.command == "receive 172.0.0.1"
    assert c.va_log.timedelta.hours == -1
    assert c.va_log.date_format == "%Y-%m-%d %H:%M:%S.%f"
    assert c.va_log.date_regex == "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    assert c.utterance_from_va.regexes[0].begin == "start_utterance"
    assert c.utterance_from_va.regexes[0].end == "end_utterance"
    assert c.format[0].key ==  "ip"
    assert c.format[0].value ==  "172.0.0.1"
