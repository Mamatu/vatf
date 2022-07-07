import logging

import json
import jsonschema
from types import SimpleNamespace

from vatf.utils import os_proxy

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

class _Config:
    def __init__(self, data):
        self.data = data
    def get(self, arg, raiseIfNotFound = True):
        return get_attr(self.data, arg, raiseIfNotFound = raiseIfNotFound)

def load_raw(config_json_pathes, schema_json_path = _abs_path_to_schema()):
    if isinstance(config_json_pathes, str):
        config_json_pathes = [config_json_pathes]
    data = None
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
            data = json.load(f, object_hook = lambda d: SimpleNamespace(**d))
            array.append(data)
    for item in array:
        if data is None:
            data = item.__dict__
        else:
            data.__dict__.update(item.__dict__)
    return _Config(data)

def load(config_json_pathes, custom_format = {}, schema_json_path = _abs_path_to_schema()):
    if isinstance(config_json_pathes, str):
        config_json_pathes = [config_json_pathes]
    c = load_raw(config_json_pathes, schema_json_path)
    def process_format(obj, format_dict):
        if hasattr(obj, "__dict__"):
            for k,v in obj.__dict__.items():
                process_format(v, format_dict)
                if isinstance(v, str):
                    try:
                        v = v.format(**format_dict)
                    except KeyError:
                        pass
                    setattr(obj, k, v)
    def make_dict(data_format):
        _dict = {}
        for kv in data_format:
            _dict[kv.key] = kv.value
        return _dict
    format_dict = {}
    if hasattr(c.data, "format") and c.data.format:
        format_dict = make_dict(c.data.format)
    if custom_format:
        format_dict.update(custom_format)
    process_format(c.data, format_dict)
    return c
