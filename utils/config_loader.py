__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import logging

import json
import jsonschema
from types import SimpleNamespace

from vatf.utils import os_proxy
from vatf.utils import config_common

def _abs_path_to_schema():
    import pathlib
    path = pathlib.Path(__file__).parent.parent.resolve()
    return os_proxy.join(path, "schemas/config.schema.json")

def get_attr(data, attr, raiseIfNotFound = True):
    if isinstance(attr, str):
        attr = attr.split(".")
    _attr = attr.copy()
    def process_attr(data):
        front = attr.pop(0)
        if front:
            value = getattr(data, front, None)
        if len(attr) == 0:
            return value
        else:
            return process_attr(value)
    output = process_attr(data)
    if output is None and raiseIfNotFound:
        raise AttributeError(f"Attr {'.'.join(_attr)} not found in config")
    return output

def _iterate_dict(dict_key, callback):
    def _make_key_chain(key_chain, key):
        new_key_chain = key_chain.copy()
        new_key_chain.append(key)
        return new_key_chain
    def iterate_dict(dict_key, callback, key_chain):
        if isinstance(dict_key, dict):
            for k,v in dict_key.items():
                dict_key[k] = iterate_dict(v, callback, key_chain = _make_key_chain(key_chain, k))
            dict_key1 = callback(key_chain, dict_key)
            return (dict_key1 if dict_key1 is not None else dict_key)
        if isinstance(dict_key, list):
            for x in range(len(dict_key)):
                dict_key[x] = iterate_dict(dict_key[x], callback, key_chain = _make_key_chain(key_chain, dict_key))
        return dict_key
    return iterate_dict(dict_key, callback, key_chain = [])

def _check(dict1, dict2):
    keys1 = dict1.keys()
    keys2 = dict2.keys()
    for k in keys2:
        if k in keys1:
            if (isinstance(dict1[k], dict) ^ isinstance(dict2[k], dict)):
                raise Exception(f"Both values of the same key must be dict or another type")
            if not (isinstance(dict1[k], dict) and isinstance(dict2[k], dict)):
                raise Exception(f"{dict1} and {dict2} contains the same keys!")

def _update_dict_deeply(obj, item):
    def callback_1(key1, dict1):
        def callback_2(key2, dict2):
            if key1 == key2 and (key1 is not None or key2 is not None):
                _check(dict1, dict2)
                temp_dict = dict1.copy()
                dict1.update(dict2)
                dict2.update(dict1)
            return dict2
        _iterate_dict(item, callback_2)
        return dict1
    return _iterate_dict(obj, callback_1)

def _convert_if_dict(obj):
    def callback(key, obj):
        return SimpleNamespace(**obj)
    return _iterate_dict(obj, callback)

def load_raw(config_json_pathes, schema_json_path = _abs_path_to_schema()):
    if isinstance(config_json_pathes, str):
        config_json_pathes = [config_json_pathes]
    array = []
    for config_json_path in config_json_pathes:
        with open(config_json_path) as f:
            logging.debug(f"Reads {config_json_path}")
            data = json.load(f)
            if schema_json_path:
                with open(schema_json_path) as schema:
                    logging.debug(f"Validation {config_json_path} by use schema {schema.name}")
                    jsonschema.validate(data, schema = json.load(schema))
        with open(config_json_path) as f:
            array.append(json.load(f))
    data = {}
    for item in array:
        data = _update_dict_deeply(data, item)
    return data

def _load_json(config_pathes, schema_json_path):
    data = load_raw(config_pathes, schema_json_path)
    return data

from vatf.utils import config_common

def load(config_pathes, schema_json_path = config_common.get_global_schema_path()):
    if isinstance(config_pathes, str):
        config_pathes = [config_pathes]
    config_json_pathes = []
    config_py_pathes = []
    for config_path in config_pathes:
        if config_path.endswith(".json"):
            config_json_pathes.append(config_path)
        elif config_path.endswith(".py"):
            config_py_pathes.append(config_path)
        else:
            config_py_pathes.append(config_path)
    c = _load_json(config_json_pathes, schema_json_path)
    from vatf.utils import config_py_loader
    c1 = config_py_loader.load(config_py_pathes)
    c.update(c1)
    return c
