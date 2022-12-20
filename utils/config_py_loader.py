import importlib
import logging
import json
import jsonschema

from vatf.utils import config_common

class Loader:
    def __init__(self, pathes, schema_path = config_common.get_global_schema_path()):
        if isinstance(pathes, str):
            pathes = [pathes]
        self.schema_path = schema_path
        self.data = self._load_configs(pathes)
    @staticmethod
    def convert_to_py_path(path):
        import os
        if ".py" in path:
            path = os.path.relpath(path)
            path = path.split('.py')[0].replace("/", ".")
        return path
    def _validate(self, data, schema_json_path):
        with open(schema_json_path) as schema:
            logging.debug(f"Validation by use schema {schema.name}")
            jsonschema.validate(data, schema = json.load(schema))
    def _load_configs(self, pathes):
        datas = [self._load_config(path) for path in pathes]
        self.data = {}
        for d in datas:
            self.data.update(d)
        return self.data
    def _load_config(self, path):
        path = Loader.convert_to_py_path(path)
        data = {}
        module = importlib.import_module(name = path)
        def has_ul_variants(f):
            return hasattr(module, f.lower()) and hasattr(module, f.upper())
        fields = [f for f in list(module.__dict__.keys()) if not f.startswith("_") and not f.startswith("__")]
        for f in fields:
            def load_field(f):
                if has_ul_variants(f):
                    raise Exception(f"config {path} contains both variants of field {f}: {f.lower()} and {f.upper()} must be one!")
                f_attr = getattr(module, f, None)
                if f_attr:
                    data[f.lower()] = f_attr
                    return True
                return False
            if not load_field(f.lower()):
                if not load_field(f.upper()):
                    logging.debug("Field: {f.lower()}/{f.upper()} not found in config {path}")
        self._validate(data, schema_json_path = self.schema_path)
        return data

from vatf.utils import config_common

def load(path, schema_path = config_common.get_global_schema_path()):
    l = Loader(path, schema_path)
    return l.data
