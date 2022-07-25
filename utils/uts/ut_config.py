import datetime
import logging
import os

from vatf.utils import config_loader
from vatf.utils import config_handler

import pytest

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
    c = config_loader.load_raw("utils/uts/data/ut_config/config.json")
    assert c.data.assets.audio.path == "./assets/audio_files"
    assert c.data.va_log.path == "/tmp/session.log"
    assert c.data.va_log.command == "receive {ip}"
    assert c.data.va_log.timedelta.hours == -1
    assert c.data.va_log.date_format == "%Y-%m-%d %H:%M:%S.%f"
    assert c.data.va_log.date_regex == "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    assert c.data.utterance_from_va.regexes[0].begin == "start_utterance"
    assert c.data.utterance_from_va.regexes[0].end == "end_utterance"
    assert c.data.format.ip ==  "172.0.0.1"

def test_load_config():
    c = config_loader.load("utils/uts/data/ut_config/config.json")
    assert c.data.assets.audio.path == "./assets/audio_files"
    assert c.data.va_log.path == "/tmp/session.log"
    assert c.data.va_log.command == "receive 172.0.0.1"
    assert c.data.va_log.timedelta.hours == -1
    assert c.data.va_log.date_format == "%Y-%m-%d %H:%M:%S.%f"
    assert c.data.va_log.date_regex == "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    assert c.data.utterance_from_va.regexes[0].begin == "start_utterance"
    assert c.data.utterance_from_va.regexes[0].end == "end_utterance"
    assert c.data.format.ip == "172.0.0.1"
    assert c.get("va_log.date_regex") == c.data.va_log.date_regex
    assert c.get("va_log.date_regex1", False) == None

def test_load_config_with_custom_format():
    c = config_loader.load("utils/uts/data/ut_config/config_custom.json", {"session_name" : "session_1"})
    assert c.data.assets.audio.path == "./assets/audio_files"
    assert c.data.va_log.path == "/session_1/session.log"
    assert c.data.va_log.command == "receive 172.0.0.1"
    assert c.data.va_log.timedelta.hours == -1
    assert c.data.va_log.date_format == "%Y-%m-%d %H:%M:%S.%f"
    assert c.data.va_log.date_regex == "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    assert c.data.utterance_from_va.regexes[0].begin == "start_utterance"
    assert c.data.utterance_from_va.regexes[0].end == "end_utterance"
    assert c.data.format.ip ==  "172.0.0.1"
    assert c.get("va_log.date_regex") == c.data.va_log.date_regex
    assert c.get("va_log.date_regex1", False) == None

def test_load_two_configs():
    c = config_loader.load(["utils/uts/data/ut_config/config1.json", "utils/uts/data/ut_config/config2.json"])
    assert c.data.assets.audio.path == "./assets/audio_files"
    assert c.data.va_log.path == "/tmp/session.log"
    assert c.data.va_log.command == "receive 172.0.0.1"
    assert c.data.va_log.timedelta.hours == -1
    assert c.data.va_log.date_format == "%Y-%m-%d %H:%M:%S.%f"
    assert c.data.va_log.date_regex == "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    assert c.data.utterance_from_va.regexes[0].begin == "start_utterance"
    assert c.data.utterance_from_va.regexes[0].end == "end_utterance"
    assert c.data.format.ip ==  "172.0.0.1"

def _handler_global_config():
    config_handler.init_configs("utils/uts/data/ut_config/config.json")
    def foo(**kwargs):
        output = config_handler.handle(["assets.audio.path", "va_log.command", "va_log.path"], custom_format = {"session_name" : "tmp"}, **kwargs)
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
    foo(config_path = "utils/uts/data/ut_config/config.json")

def test_handler_config():
    config = config_loader.load("utils/uts/data/ut_config/config.json")
    def foo(**kwargs):
        output = config_handler.handle(["assets.audio.path", "va_log.command", "va_log.path"], **kwargs)
        assert output["assets.audio.path"] == "./assets/audio_files"
        assert output["va_log.command"] == "receive 172.0.0.1"
        assert output["va_log.path"] == "/tmp/session.log"
    foo(config = config)

def test_handler_config_attrs():
    config_attrs = {"assets.audio.path" : "./assets/audio_files", "va_log.command" : "receive 172.0.0.1", "va_log.path" : "/tmp/session.log"}
    def foo(**kwargs):
        output = config_handler.handle(["assets.audio.path", "va_log.command", "va_log.path"], **kwargs)
        assert output["assets.audio.path"] == "./assets/audio_files"
        assert output["va_log.command"] == "receive 172.0.0.1"
        assert output["va_log.path"] == "/tmp/session.log"
    foo(config_attrs = config_attrs)

def _handler_global_config_custom():
    config_handler.init_configs("utils/uts/data/ut_config/config_custom.json")
    def foo(**kwargs):
        output = config_handler.handle(["assets.audio.path", "va_log.command", "va_log.path"], **kwargs)
        assert output["assets.audio.path"] == "./assets/audio_files"
        assert output["va_log.command"] == "receive 172.0.0.1"
        assert output["va_log.path"] == "/tmp/session.log"
    foo()

def test_handler_config_path_custom():
    def foo(**kwargs):
        output = config_handler.handle(["assets.audio.path", "va_log.command", "va_log.path"], custom_format = {"session_name" : "tmp"}, **kwargs)
        assert output["assets.audio.path"] == "./assets/audio_files"
        assert output["va_log.command"] == "receive 172.0.0.1"
        assert output["va_log.path"] == "/tmp/session.log"
    foo(config_path = "utils/uts/data/ut_config/config_custom.json")

def test_handler_config_custom():
    config = config_loader.load("utils/uts/data/ut_config/config_custom.json", custom_format = {"session_name" : "tmp"})
    def foo(**kwargs):
        output = config_handler.handle(["assets.audio.path", "va_log.command", "va_log.path"], custom_format = {"session_name" : "tmp"}, **kwargs)
        assert output["assets.audio.path"] == "./assets/audio_files"
        assert output["va_log.command"] == "receive 172.0.0.1"
        assert output["va_log.path"] == "/tmp/session.log"
    foo(config = config)

def _handler_global_config_custom_format():
    config_handler.init_configs("utils/uts/data/ut_config/config_custom_without_format.json")
    def foo(**kwargs):
        output = config_handler.handle(["assets.audio.path", "va_log.command", "va_log.path"], custom_format = {"ip" : "172.0.0.1"}, **kwargs)
        assert output["assets.audio.path"] == "./assets/audio_files"
        assert output["va_log.command"] == "receive 172.0.0.1"
        assert output["va_log.path"] == "/tmp/session.log"
    foo()

def test_handler_config_path_custom_format():
    def foo(**kwargs):
        output = config_handler.handle(["assets.audio.path", "va_log.command", "va_log.path"], custom_format = {"ip" : "172.0.0.1", "session_name" : "tmp"}, **kwargs)
        assert output["assets.audio.path"] == "./assets/audio_files"
        assert output["va_log.command"] == "receive 172.0.0.1"
        assert output["va_log.path"] == "/tmp/session.log"
    foo(config_path = "utils/uts/data/ut_config/config_custom_without_format.json")

def test_handler_config_custom_format():
    config = config_loader.load("utils/uts/data/ut_config/config_custom_without_format.json", custom_format = {"ip" : "172.0.0.1", "session_name" : "tmp"})
    def foo(**kwargs):
        output = config_handler.handle(["assets.audio.path", "va_log.command", "va_log.path"], custom_format = {"ip" : "172.0.0.1", "session_name" : "tmp"}, **kwargs)
        assert output["assets.audio.path"] == "./assets/audio_files"
        assert output["va_log.command"] == "receive 172.0.0.1"
        assert output["va_log.path"] == "/tmp/session.log"
    foo(config = config)

def test_handler_config_attrs_custom_format():
    config_attrs = {"assets.audio.path" : "./assets/audio_files", "va_log.command" : "receive {ip}", "va_log.path" : "/tmp/session.log"}
    def foo(**kwargs):
        output = config_handler.handle(["assets.audio.path", "va_log.command", "va_log.path"], custom_format = {"ip" : "172.0.0.1"}, **kwargs)
        assert output["assets.audio.path"] == "./assets/audio_files"
        assert output["va_log.command"] == "receive 172.0.0.1"
        assert output["va_log.path"] == "/tmp/session.log"
    foo(config_attrs = config_attrs)

def test_handler_2_configs():
    config_handler.init_configs(["utils/uts/data/ut_config/config_custom_without_format.json", "utils/uts/data/ut_config/config_format.json"])
    def foo(**kwargs):
        output = config_handler.handle(["assets.audio.path", "va_log.command", "va_log.path", "format.ip"], **kwargs)
        assert output["assets.audio.path"] == "./assets/audio_files"
        assert output["va_log.command"] == "receive 172.0.0.1"
        assert output["va_log.path"] == "/tmp/session.log"
        assert output["format.ip"] == "172.0.0.1"
    foo()

def test_merge_2_formats():
    c1 = {"format" : {"key1" : "value1"}}
    c2 = {"format" : {"key2" : "value2"}}
    assert {"format" : {"key1" : "value1", "key2" : "value2"}} == config_loader._update_dict_deeply(c1, c2)
    config_handler.init_configs(["utils/uts/data/ut_config/format2.json", "utils/uts/data/ut_config/format1.json"])
    def foo(**kwargs):
        output = config_handler.handle(["format.key1", "format.key2"], **kwargs)
        assert output["format.key2"] == "value2"
        assert output["format.key1"] == "value1"
    foo()

def test_iterate_dict_not_modified_obj(mocker):
    mock = mocker.Mock()
    def callback(key, obj):
        mock(obj)
    dict_1 = {"key1" : "value1"}
    output = config_loader._iterate_dict(dict_1, callback)
    mock.assert_called_once_with(dict_1)
    assert dict_1 == output

def test_iterate_dict_modified_obj(mocker):
    mock = mocker.Mock()
    def callback(key, obj):
        mock(obj)
        obj.update({"key2" : "value2"})
        return obj
    dict_1 = {"key1" : "value1"}
    expected_dict = {"key1" : "value1", "key2" : "value2"}
    output = config_loader._iterate_dict(dict_1, callback)
    mock.assert_called_once_with(dict_1)
    assert expected_dict == output

def test_update_dict_deeply_empty(mocker):
    dict_1 = {}
    dict_2 = {}
    d = config_loader._update_dict_deeply(dict_1, dict_2)
    assert d == {}

def test_update_dict_deeply_trival(mocker):
    dict_1 = {}
    dict_2 = {"key" : "value"}
    d = config_loader._update_dict_deeply(dict_1, dict_2)
    assert d == {"key" : "value"}

def test_update_dict_deeply_trival_1(mocker):
    dict_1 = {"key1" : "value1"}
    dict_2 = {"key2" : "value2"}
    d = config_loader._update_dict_deeply(dict_1, dict_2)
    assert d == {"key1" : "value1", "key2" : "value2"}

def test_update_dict_deeply_trival_2(mocker):
    dict_1 = {"d" : {"key1" : "value1"}}
    dict_2 = {"d" : {"key2" : "value2"}}
    d = config_loader._update_dict_deeply(dict_1, dict_2)
    assert d == {"d" : {"key1" : "value1", "key2" : "value2"}}

def test_update_dict_deeply_init(mocker):
    dict_1 = {}
    dict_2 = {"dict21" : {"key211" : "value211"}}
    d = config_loader._update_dict_deeply(dict_1, dict_2)
    assert d == {"dict21" : {"key211" : "value211"}}

def test_update_dict_deeply_two_different(mocker):
    dict_1 = {"dict11" : {"key111" : "value111"}}
    dict_2 = {"dict21" : {"key211" : "value211"}}
    d = config_loader._update_dict_deeply(dict_1, dict_2)
    assert d == {"dict11" : {"key111" : "value111"}, "dict21" : {"key211" : "value211"}}

def test_update_dict_deeply_1(mocker):
    dict_1 = {"dict1" : {"key1" : "value1"}}
    dict_2 = {"dict1" : {"key2" : "value2"}}
    d = config_loader._update_dict_deeply(dict_1, dict_2)
    assert d == {"dict1" : {"key1" : "value1", "key2" : "value2"}}

def test_update_dict_deeply_2(mocker):
    dict_1 = {"dict1" : {"key1" : "value1"}}
    dict_2 = {"dict1" : {"dict2" : { "dict1" : {"key2" : "value2"}}}}
    d = config_loader._update_dict_deeply(dict_1, dict_2)
    assert d == {"dict1" : {"key1" : "value1", "dict2" : { "dict1" : { "key2" : "value2"}}}}

def test_update_dict_deeply_exception_diff_values_for_the_same_key(mocker):
    dict_1 = {"dict1" : {"key1" : "value1"}}
    dict_2 = {"dict1" : {"key1" : "value2"}}
    with pytest.raises(Exception) as e:
        d = config_loader._update_dict_deeply(dict_1, dict_2)

def test_iterate_dict_update_deeply_deep(mocker):
    dict_1 = {"dict1" : {"key1" : {"key11" : "value11"}}}
    dict_2 = {"dict1" : {"key1" : {"key12" : "value12"}}}
    d = config_loader._update_dict_deeply(dict_1, dict_2)
    assert d == {"dict1" : {"key1" : {"key11" : "value11", "key12" : "value12"}}}

def test_load_config_with_formats_1(mocker):
    config_handler.init_configs(["utils/uts/data/ut_config/config_ff.json", "utils/uts/data/ut_config/format1.json", "utils/uts/data/ut_config/format2.json"])
    def foo(**kwargs):
        output = config_handler.handle(["assets.audio.path"], **kwargs)
        assert output["assets.audio.path"] == "/value1/value2"
    foo()

from contextlib import contextmanager
from unittest.mock import patch

# Source: https://stackoverflow.com/a/46919967
@contextmanager
def mocked_now(now):
    class MockedDatetime(datetime.datetime):
        @classmethod
        def now(cls):
            return now
    with patch("datetime.datetime", MockedDatetime):
        yield

def test_load_config_with_formats_2(mocker):
    with mocked_now(datetime.datetime(2020, 2, 2)):
        config_handler.init_configs(["utils/uts/data/ut_config/config_ff_1.json", "utils/uts/data/ut_config/format1.json", "utils/uts/data/ut_config/format2.json"])
        def foo(**kwargs):
            output = config_handler.handle(["assets.audio.path", "va_log.path"], **kwargs)
            assert output["assets.audio.path"] == "/value1/value2"
            assert output["va_log.path"] == "/2020_02_02_00_00_00/value1/session.log"
        foo()

def test_use_case_1(mocker):
    ut_data_path = "./utils/uts/data/ut_config/test_use_case_1"
    with mocked_now(datetime.datetime(2020, 2, 2)):
        config_handler.init_configs([os.path.join(ut_data_path, "config.json"), os.path.join(ut_data_path, "mgu_config.json"), os.path.join(ut_data_path, "filter_speechcore.json")])
        def foo(**kwargs):
            output = config_handler.handle(["va_log.path", "va_log.command"], **kwargs)
            assert output["va_log.path"] == "/tmp/data/session_2020_02_02_00_00_00/log/session.log"
            expected_command = "bash -c \"dlt-receive -o /tmp/data/session_2020_02_02_00_00_00/log/session.log.dlt -a 192.168.150.20 > >(tee /tmp/data/session_2020_02_02_00_00_00/log/session.log | grep \"SPEE\")\""
            assert output["va_log.command"] == expected_command
        foo()
