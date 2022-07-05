import datetime
import logging
import os

from vatf.utils import config_loader

def test_get():
    class Attr1:
        def __init__(self):
            self.attr2 = 3
    class Data:
        def __init__(self):
            self.attr1 = Attr1()
    data = Data()
    assert config_loader.get(data, "attr1.attr2") == 3
    assert config_loader.get(data, "attr1.attr3", False) == None

def test_load_config_raw():
    c = config_loader.load_raw("utils/uts/config.json")
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
    c = config_loader.load("utils/uts/config.json")
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
    assert config_loader.get(c, "va_log.date_regex") == c.va_log.date_regex
    assert config_loader.get(c, "va_log.date_regex1", False) == None

def test_load_config_with_custom_format():
    c = config_loader.load("utils/uts/config_custom.json", {"session_name" : "session_1"})
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
    assert config_loader.get(c, "va_log.date_regex") == c.va_log.date_regex
    assert config_loader.get(c, "va_log.date_regex1", False) == None

def test_load_two_configs():
    c = config_loader.load(["utils/uts/config1.json", "utils/uts/config2.json"])
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
