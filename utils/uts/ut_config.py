__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

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
    assert c["assets"]["audio"]["path"] == "./assets/audio_files"
    assert c["va_log"]["path"] == "/tmp/session.log"
    assert c["va_log"]["command"] == "receive {ip}"
    assert c["va_log"]["timedelta"]["hours"] == -1
    assert c["va_log"]["date_format"] == "%Y-%m-%d %H:%M:%S.%f"
    assert c["va_log"]["date_regex"] == "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    assert c["utterance_from_va"]["regexes"][0]["begin"] == "start_utterance"
    assert c["utterance_from_va"]["regexes"][0]["end"] == "end_utterance"
    assert c["format"]["ip"] ==  "172.0.0.1"

def test_load_config():
    c = config_loader.load("utils/uts/data/ut_config/config.json")
    c = config_handler.Config(c)
    assert c.assets.audio.path == "./assets/audio_files"
    assert c.va_log.path == "/tmp/session.log"
    assert c.va_log.command == "receive 172.0.0.1"
    assert c.va_log.timedelta.hours == -1
    assert c.va_log.date_format == "%Y-%m-%d %H:%M:%S.%f"
    assert c.va_log.date_regex == "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    assert c.utterance_from_va.regexes[0].begin == "start_utterance"
    assert c.utterance_from_va.regexes[0].end == "end_utterance"
    assert c.format.ip == "172.0.0.1"
    assert c.get("va_log.date_regex") == c.va_log.date_regex
    assert c.get("va_log.date_regex1", False) == None

def test_load_config_with_custom_format():
    c = config_loader.load("utils/uts/data/ut_config/config_custom.json")
    c = config_handler.Config(c, {"session_name" : "session_1"})
    assert c.assets.audio.path == "./assets/audio_files"
    assert c.va_log.path == "/session_1/session.log"
    assert c.va_log.command == "receive 172.0.0.1"
    assert c.va_log.timedelta.hours == -1
    assert c.va_log.date_format == "%Y-%m-%d %H:%M:%S.%f"
    assert c.va_log.date_regex == "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    assert c.utterance_from_va.regexes[0].begin == "start_utterance"
    assert c.utterance_from_va.regexes[0].end == "end_utterance"
    assert c.format.ip ==  "172.0.0.1"
    assert c.get("va_log.date_regex") == c.va_log.date_regex
    assert c.get("va_log.date_regex1", False) == None

def test_load_two_configs():
    c = config_loader.load(["utils/uts/data/ut_config/config1.json", "utils/uts/data/ut_config/config2.json"])
    c = config_handler.Config(c)
    assert c.assets.audio.path == "./assets/audio_files"
    assert c.va_log.path == "/tmp/session.log"
    assert c.va_log.command == "receive 172.0.0.1"
    assert c.va_log.timedelta.hours == -1
    assert c.va_log.date_format == "%Y-%m-%d %H:%M:%S.%f"
    assert c.va_log.date_regex == "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
    assert c.utterance_from_va.regexes[0].begin == "start_utterance"
    assert c.utterance_from_va.regexes[0].end == "end_utterance"
    assert c.format.ip ==  "172.0.0.1"

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
    config = config_loader.load("utils/uts/data/ut_config/config_custom.json")
    def foo(**kwargs):
        output = config_handler.handle(["assets.audio.path", "va_log.command", "va_log.path"], custom_format = {"session_name" : "tmp"}, **kwargs)
        assert output["assets.audio.path"] == "./assets/audio_files"
        assert output["va_log.command"] == "receive 172.0.0.1"
        assert output["va_log.path"] == "/tmp/session.log"
    foo(config = config)

def test_handler_global_config_custom_format():
    config_handler.init_configs("utils/uts/data/ut_config/config_custom_without_format.json")
    def foo(**kwargs):
        output = config_handler.handle(["assets.audio.path", "va_log.command", "va_log.path"], custom_format = {"ip" : "172.0.0.1", "session_name" : "tmp"}, **kwargs)
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
    config = config_loader.load("utils/uts/data/ut_config/config_custom_without_format.json")
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
        config_handler.init_configs([os.path.join(ut_data_path, "config.json"), os.path.join(ut_data_path, "ip_config.json"), os.path.join(ut_data_path, "filter_speechcore.json")])
        def foo(**kwargs):
            output = config_handler.handle(["va_log.path", "va_log.command"], **kwargs)
            assert output["va_log.path"] == "/tmp/data/session_2020_02_02_00_00_00/log/session.log"
            expected_command = "bash -c \"dlt-receive -o /tmp/data/session_2020_02_02_00_00_00/log/session.log.dlt -a 192.168.150.20 > >(tee /tmp/data/session_2020_02_02_00_00_00/log/session.log | grep \"SPEE\")\""
            assert output["va_log.command"] == expected_command
        foo()

def test_use_case_2(mocker):
    ut_data_path = "./utils/uts/data/ut_config/test_use_case_2"
    with mocked_now(datetime.datetime(2020, 2, 2)):
        config_json = os.path.join(ut_data_path, "config.json")
        ip_config_json = os.path.join(ut_data_path, "ip_config.json")
        filter_speechcore_json = os.path.join(ut_data_path, "filter_speechcore.json")
        config_handler.init_configs([config_json, ip_config_json, filter_speechcore_json], custom_format = {"test_name" : "test_use_case_2"})
        def foo(**kwargs):
            output = config_handler.handle(["va_log.path", "va_log.command"], **kwargs)
            assert output["va_log.path"] == "/tmp/data/test_use_case_2/session_2020_02_02_00_00_00/log/session.log"
            expected_command = "bash -c \"dlt-receive -o /tmp/data/test_use_case_2/session_2020_02_02_00_00_00/log/session.log.dlt -a 192.168.150.20 > >(tee /tmp/data/test_use_case_2/session_2020_02_02_00_00_00/log/session.log | grep \"SPEE\")\""
            assert output["va_log.command"] == expected_command
        foo()

def test_py_config():
    from vatf.utils import config_py_loader
    import pathlib
    import logging
    logging.basicConfig(level = logging.DEBUG)
    config_py_path = "utils.uts.data.ut_config.config_1"
    config = config_py_loader.load(config_py_path)
    assert config["assets"]["audio"]["path"] == "./assets/audio_files"

def test_py_config_1():
    from vatf.utils import config_py_loader
    import pathlib
    import logging
    logging.basicConfig(level = logging.DEBUG)
    config_py_path = "utils/uts/data/ut_config/config_1.py"
    config = config_py_loader.load(config_py_path)
    assert config["assets"]["audio"]["path"] == "./assets/audio_files"

def test_py_config_2():
    from vatf.utils import config_py_loader
    import pathlib
    import logging
    logging.basicConfig(level = logging.DEBUG)
    config_py_path = "utils.uts.data.ut_config.config_1"
    config_handler.init_configs([config_py_path])
    output = config_handler.handle(["assets.audio.path"])
    assert output["assets.audio.path"] == "./assets/audio_files"

def test_py_config_3():
    from vatf.utils import config_py_loader
    import pathlib
    import logging
    logging.basicConfig(level = logging.DEBUG)
    config_py_path = "utils/uts/data/ut_config/config_1.py"
    config_handler.init_configs([config_py_path])
    output = config_handler.handle(["assets.audio.path"])
    assert output["assets.audio.path"] == "./assets/audio_files"

def test_new_config_impl_handler_global_config():
    config_handler.init_configs("utils/uts/data/ut_config/config.json")
    def foo(**kwargs):
        config = config_handler.get_config(custom_format = {"session_name" : "tmp"}, **kwargs)
        assert config.assets.audio.path == "./assets/audio_files"
        assert config.va_log.command == "receive 172.0.0.1"
        assert config.va_log.path == "/tmp/session.log"
    foo()

def test_new_config_handler_config_path():
    def foo(**kwargs):
        config = config_handler.get_config(**kwargs)
        assert config.assets.audio.path == "./assets/audio_files"
        assert config.va_log.command == "receive 172.0.0.1"
        assert config.va_log.path == "/tmp/session.log"
    foo(config_path = "utils/uts/data/ut_config/config.json")

def test_new_config_handler_config():
    config = config_loader.load("utils/uts/data/ut_config/config.json")
    def foo(**kwargs):
        config = config_handler.get_config(**kwargs)
        assert config.assets.audio.path == "./assets/audio_files"
        assert config.va_log.command == "receive 172.0.0.1"
        assert config.va_log.path == "/tmp/session.log"
    foo(config = config)

def test_new_config_handler_config_attrs_1():
    config_dict = {"va_log.command" : "receive 172.0.0.1", "va_log.path" : "/tmp/session.log"}
    def foo(**kwargs):
        config = config_handler.get_config(**kwargs)
        assert config.va_log.command == "receive 172.0.0.1"
        assert config.va_log.path == "/tmp/session.log"
    foo(config_dict = config_dict)
    foo(config_attrs = config_dict)
    foo(config = config_dict)

def test_new_config_handler_config_attrs_2():
    config_dict = {"assets.audio.path" : "./assets/audio_files", "va_log.command" : "receive 172.0.0.1", "va_log.path" : "/tmp/session.log"}
    def foo(**kwargs):
        config = config_handler.get_config(**kwargs)
        assert config.assets.audio.path == "./assets/audio_files"
        assert config.va_log.command == "receive 172.0.0.1"
        assert config.va_log.path == "/tmp/session.log"
    foo(config_dict = config_dict)
    foo(config_attrs = config_dict)
    foo(config = config_dict)

def test_new_config_handler_config_attrs_3():
    config_dict = {"assets.audio.path" : "./assets/audio_files"}
    def foo(**kwargs):
        config = config_handler.get_config(**kwargs)
        assert config.assets.audio.path == "./assets/audio_files"
    foo(config = config_dict)
    foo(config_dict = config_dict)
    foo(config_attrs = config_dict)

def test_new_config_handler_global_config_custom():
    config_handler.init_configs("utils/uts/data/ut_config/config_custom.json")
    def foo(**kwargs):
        config = config_handler.get_config(**kwargs)
        assert config.assets.audio.path == "./assets/audio_files"
        assert config.va_log.command == "receive 172.0.0.1"
        assert config.va_log.path == "/tmp/session.log"
    foo()

def test_new_config_handler_config_path_custom():
    def foo(**kwargs):
        config = config_handler.get_config(custom_format = {"session_name" : "data"}, **kwargs)
        assert config.assets.audio.path == "./assets/audio_files"
        assert config.va_log.command == "receive 172.0.0.1"
        assert config.va_log.path == "/data/session.log"
    foo(config_path = "utils/uts/data/ut_config/config_custom.json")

def test_new_config_handler_config_custom():
    config = config_loader.load("utils/uts/data/ut_config/config_custom.json")
    def foo(**kwargs):
        config = config_handler.get_config(custom_format = {"session_name" : "data"}, **kwargs)
        assert config.assets.audio.path == "./assets/audio_files"
        assert config.va_log.command == "receive 172.0.0.1"
        assert config.va_log.path == "/data/session.log"
    foo(config = config)

def test_new_config_handler_config_path_custom_format():
    def foo(**kwargs):
        config = config_handler.get_config(custom_format = {"ip" : "172.0.0.1", "session_name" : "tmp"}, **kwargs)
        assert config.assets.audio.path == "./assets/audio_files"
        assert config.va_log.command == "receive 172.0.0.1"
        assert config.va_log.path == "/tmp/session.log"
    foo(config_path = "utils/uts/data/ut_config/config_custom_without_format.json")

def test_new_config_handler_config_custom_format():
    config = config_loader.load("utils/uts/data/ut_config/config_custom_without_format.json")
    def foo(**kwargs):
        config = config_handler.get_config(custom_format = {"ip" : "172.0.0.1", "session_name" : "tmp"}, **kwargs)
        assert config.assets.audio.path == "./assets/audio_files"
        assert config.va_log.command == "receive 172.0.0.1"
        assert config.va_log.path == "/tmp/session.log"
    foo(config = config)

def test_handler_config_attrs_custom_format():
    config_attrs = {"assets.audio.path" : "./assets/audio_files", "va_log.command" : "receive {ip}", "va_log.path" : "/tmp/session.log"}
    def foo(**kwargs):
        config = config_handler.get_config(custom_format = {"ip" : "172.0.0.1"}, **kwargs)
        assert config.assets.audio.path == "./assets/audio_files"
        assert config.va_log.command == "receive 172.0.0.1"
        assert config.va_log.path == "/tmp/session.log"
    foo(config_attrs = config_attrs)

def test_handler_2_configs():
    config_handler.init_configs(["utils/uts/data/ut_config/config_custom_without_format.json", "utils/uts/data/ut_config/config_format.json"])
    def foo(**kwargs):
        config = config_handler.get_config(**kwargs)
        assert config.assets.audio.path == "./assets/audio_files"
        assert config.va_log.command == "receive 172.0.0.1"
        assert config.va_log.path == "/tmp/session.log"
        assert config.format.ip == "172.0.0.1"
    foo()

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
        config_handler.init_configs([os.path.join(ut_data_path, "config.json"), os.path.join(ut_data_path, "ip_config.json"), os.path.join(ut_data_path, "filter_speechcore.json")])
        def foo(**kwargs):
            config = config_handler.get_config(**kwargs)
            assert config.va_log.path == "/tmp/data/session_2020_02_02_00_00_00/log/session.log"
            expected_command = "bash -c \"dlt-receive -o /tmp/data/session_2020_02_02_00_00_00/log/session.log.dlt -a 192.168.150.20 > >(tee /tmp/data/session_2020_02_02_00_00_00/log/session.log | grep \"SPEE\")\""
            assert config.va_log.command == expected_command
        foo()

def test_use_case_2(mocker):
    ut_data_path = "./utils/uts/data/ut_config/test_use_case_2"
    with mocked_now(datetime.datetime(2020, 2, 2)):
        config_json = os.path.join(ut_data_path, "config.json")
        ip_config_json = os.path.join(ut_data_path, "ip_config.json")
        filter_speechcore_json = os.path.join(ut_data_path, "filter_speechcore.json")
        config_handler.init_configs([config_json, ip_config_json, filter_speechcore_json], custom_format = {"test_name" : "test_use_case_2"})
        def foo(**kwargs):
            config = config_handler.get_config(**kwargs)
            assert config.va_log.path == "/tmp/data/test_use_case_2/session_2020_02_02_00_00_00/log/session.log"
            expected_command = "bash -c \"dlt-receive -o /tmp/data/test_use_case_2/session_2020_02_02_00_00_00/log/session.log.dlt -a 192.168.150.20 > >(tee /tmp/data/test_use_case_2/session_2020_02_02_00_00_00/log/session.log | grep \"SPEE\")\""
            assert config.va_log.command == expected_command
        foo()

def test_use_case_3(mocker):
    ut_data_path = "./utils/uts/data/ut_config/test_use_case_3"
    with mocked_now(datetime.datetime(2020, 2, 2, 23, 45, 50)):
        config_path = os.path.join(ut_data_path, "config.py")
        config_handler.init_configs([config_path])
        def foo(**kwargs):
            config = config_handler.get_config(**kwargs)
            assert config.vatf.branch == "develop_20220815"
            assert config.audio.path == "/tmp/data/session_2020_02_02_23_45_50/audio"
            assert config.assets.audio.path == "./assets/audio_files"
            assert len(config.assets.audio.files) == 2
            assert config.assets.audio.files[0].name == "alexa_are_you_there.wav"
            assert config.assets.audio.files[0].tags[0] == "verification"
            assert config.assets.audio.files[1].name == "alexa_tell_me_a_joke.wav"
            assert config.assets.audio.files[1].tags[0] == "joke"
            date_format = "%Y-%m-%d %H:%M:%S.%f"
            date_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
            assert config.va_log.path == "/tmp/data/session_2020_02_02_23_45_50/log/session.log"
            assert config.va_log.timedelta.hours == -1
            assert config.va_log.date_format == date_format
            assert config.va_log.date_regex == date_regex
            assert config.wait_for_regex.path == "/tmp/data/session_2020_02_02_23_45_50/log/session.log"
            assert config.wait_for_regex.date_format == date_format
            assert config.wait_for_regex.date_regex == date_regex
            assert len(config.utterance_from_va.regexes) == 1
            assert config.utterance_from_va.regexes[0].begin == "DialogUXStateAggregator:executeSetState:from=THINKING,to=SPEAKING,validTransition=true"
            assert config.utterance_from_va.regexes[0].end == "DialogUXStateAggregator:executeSetState:from=SPEAKING,to=IDLE,validTransition=true"
        foo()

def test_use_case_4(mocker):
    ut_data_path = "./utils/uts/data/ut_config/test_use_case_4"
    with mocked_now(datetime.datetime(2020, 2, 2, 23, 45, 50)):
        config_path = os.path.join(ut_data_path, "config.json")
        config_handler.init_configs([config_path])
        def foo(**kwargs):
            config = config_handler.get_config(**kwargs)
            assert config.vatf.branch == "develop_20220815"
            assert config.audio.path == "/tmp/data/session_2020_02_02_23_45_50/audio"
            assert config.assets.audio.path == "./assets/audio_files"
            assert len(config.assets.audio.files) == 2
            assert config.assets.audio.files[0].name == "alexa_are_you_there.wav"
            assert config.assets.audio.files[0].tags[0] == "verification"
            assert config.assets.audio.files[1].name == "alexa_tell_me_a_joke.wav"
            assert config.assets.audio.files[1].tags[0] == "joke"
            date_format = "%Y-%m-%d %H:%M:%S.%f"
            date_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"
            assert config.va_log.path == "/tmp/data/session_2020_02_02_23_45_50/log/session.log"
            assert config.va_log.timedelta.hours == -1
            assert config.va_log.date_format == date_format
            assert config.va_log.date_regex == date_regex
            assert config.wait_for_regex.path == "/tmp/data/session_2020_02_02_23_45_50/log/session.log"
            assert config.wait_for_regex.date_format == date_format
            assert config.wait_for_regex.date_regex == date_regex
            assert len(config.utterance_from_va.regexes) == 1
            assert config.utterance_from_va.regexes[0].begin == "DialogUXStateAggregator:executeSetState:from=THINKING,to=SPEAKING,validTransition=true"
            assert config.utterance_from_va.regexes[0].end == "DialogUXStateAggregator:executeSetState:from=SPEAKING,to=IDLE,validTransition=true"
        foo()
