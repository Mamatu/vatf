import datetime
import logging
import os

from vatf.utils import config_loader
from vatf.utils import config_handler

def test_get():
    class Attr1:
        def __init__(self):
            self.attr2 = 3
    class Data:
        def __init__(self):
            self.attr1 = Attr1()
    data = Data()
    assert config_loader.get_attr(data, "attr1.attr2") == 3
    assert config_loader.get_attr(data, "attr1.attr3", False) == None

def teardown_module():
    config_handler.reset_configs()

def test_load_config_raw():
    c = config_loader.load_raw("utils/uts/config.json")
    assert c.data.assets.audio.path == "./assets/audio_files"
    assert c.data.va_log.path == "/tmp/session.log"
    assert c.data.va_log.command == "receive {ip}"
    assert c.data.va_log.timedelta.hours == -1
    assert c.data.va_log.date_format == "%Y-%m-%d %H:%M:%S.%f"
    assert c.data.va_log.date_regex == "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    assert c.data.utterance_from_va.regexes[0].begin == "start_utterance"
    assert c.data.utterance_from_va.regexes[0].end == "end_utterance"
    assert c.data.format[0].key ==  "ip"
    assert c.data.format[0].value ==  "172.0.0.1"

def test_load_config():
    c = config_loader.load("utils/uts/config.json")
    assert c.data.assets.audio.path == "./assets/audio_files"
    assert c.data.va_log.path == "/tmp/session.log"
    assert c.data.va_log.command == "receive 172.0.0.1"
    assert c.data.va_log.timedelta.hours == -1
    assert c.data.va_log.date_format == "%Y-%m-%d %H:%M:%S.%f"
    assert c.data.va_log.date_regex == "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    assert c.data.utterance_from_va.regexes[0].begin == "start_utterance"
    assert c.data.utterance_from_va.regexes[0].end == "end_utterance"
    assert c.data.format[0].key ==  "ip"
    assert c.data.format[0].value ==  "172.0.0.1"
    assert c.get("va_log.date_regex") == c.data.va_log.date_regex
    assert c.get("va_log.date_regex1", False) == None

def test_load_config_with_custom_format():
    c = config_loader.load("utils/uts/config_custom.json", {"session_name" : "session_1"})
    assert c.data.assets.audio.path == "./assets/audio_files"
    assert c.data.va_log.path == "/session_1/session.log"
    assert c.data.va_log.command == "receive 172.0.0.1"
    assert c.data.va_log.timedelta.hours == -1
    assert c.data.va_log.date_format == "%Y-%m-%d %H:%M:%S.%f"
    assert c.data.va_log.date_regex == "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    assert c.data.utterance_from_va.regexes[0].begin == "start_utterance"
    assert c.data.utterance_from_va.regexes[0].end == "end_utterance"
    assert c.data.format[0].key ==  "ip"
    assert c.data.format[0].value ==  "172.0.0.1"
    assert c.get("va_log.date_regex") == c.data.va_log.date_regex
    assert c.get("va_log.date_regex1", False) == None

def test_load_two_configs():
    c = config_loader.load(["utils/uts/config1.json", "utils/uts/config2.json"])
    assert c.data.assets.audio.path == "./assets/audio_files"
    assert c.data.va_log.path == "/tmp/session.log"
    assert c.data.va_log.command == "receive 172.0.0.1"
    assert c.data.va_log.timedelta.hours == -1
    assert c.data.va_log.date_format == "%Y-%m-%d %H:%M:%S.%f"
    assert c.data.va_log.date_regex == "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    assert c.data.utterance_from_va.regexes[0].begin == "start_utterance"
    assert c.data.utterance_from_va.regexes[0].end == "end_utterance"
    assert c.data.format[0].key ==  "ip"
    assert c.data.format[0].value ==  "172.0.0.1"

def _handler_global_config():
    config_handler.init_configs("utils/uts/config.json")
    def foo(**kwargs):
        output = config_handler.handle(["assets.audio.path", "va_log.command", "va_log.path"], **kwargs)
        assert output["assets.audio.path"] == "./assets/audio_files"
        assert output["va_log.command"] == "receive 172.0.0.1"
        assert output["va_log.path"] == "/tmp/session.log"
    foo()

def test_handler_config_path():
    def foo(**kwargs):
        output = config_handler.handle(["assets.audio.path", "va_log.command", "va_log.path"], **kwargs)
        assert output["assets.audio.path"] == "./assets/audio_files"
        assert output["va_log.command"] == "receive 172.0.0.1"
        assert output["va_log.path"] == "/tmp/session.log"
    foo(config_path = "utils/uts/config.json")
