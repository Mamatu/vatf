import json
import jsonschema
from jsonschema import validate
import logging
import os

from vatf.utils import os_proxy

class Vatf:
    def __init__(self, data):
        vatf = data["vatf"]
        self.branch = vatf["branch"]
    @staticmethod
    def create(data):
        if not "vatf" in data:
            return None
        return Vatf(data)

class AudioFile:
    def __init__(self, file_obj):
        self.name = file_obj['name']
        self.tags = file_obj['tags']

class Audio:
    def __init__(self, data):
        self.data = data
        audio = data["audio"]
        self.path = audio["path"]
        files = audio['files']
        self.files = [AudioFile(f) for f in files]

class Assets:
    def __init__(self, data):
        self.data = data
        assets = data['assets']
        self.audio = Audio(assets)

class UtteranceRegexInLog:
    def __init__(self, data):
        self.begin = data['begin']
        self.end = data['end']

class UtteranceFromVA:
    def __init__(self, data):
        self.regexes = []
        data = data['utterance_from_va']
        if data:
            regexes = data['regexes']
            if regexes:
                self.regexes = [UtteranceRegexInLog(r) for r in regexes]
    @staticmethod
    def create(data):
        if 'utterance_from_va' in data:
            return UtteranceFromVA(data)
        return None

class UtteranceToVA:
    def __init__(self, data):
        self.regexes = []
        data = data['utterance_to_va']
        if data:
            regexes = data['regexes']
            if regexes:
                self.regexes = [UtteranceRegexInLog(r) for r in regexes]
    @staticmethod
    def create(data):
        if 'utterance_to_va' in data:
            return UtteranceToVA(data)
        return None

class VaLog:
    def __init__(self, data):
        import datetime
        va_log = data["va_log"]
        self.path = va_log["path"]
        self.timedelta = datetime.timedelta(**va_log["timedelta"])

class Config:
    def __init__(self, config_json_path = None, schema_json_path = None):
        with open(config_json_path) as f:
            logging.debug(f"Reads {config_json_path}")
            data = json.load(f)
            self.data = data
            if schema_json_path:
                with open(schema_json_path) as schema:
                    logging.debug(f"Validation {config_json_path} by use schema {schema.name}")
                    validate(data, schema=json.load(schema))
            self.vatf = Vatf.create(data)
            self.assets = Assets(data)
            self.va_log = VaLog(data)
            self.utterance_from_va = UtteranceFromVA.create(data)
            self.utterance_to_va = UtteranceToVA.create(data)
            self.searched_audio_files_pathes = self.assets.audio.path
    def get_copy(self):
        import copy
        return copy.deepcopy(self)
    def get_vatf_branch_to_clone(self):
        if self.vatf == None:
            return ""
        return self.vatf.branch
    def get_pathes_audio_files(self):
        return [self.assets.audio.path]
    def _convert_to_zone(self, dt, op):
        if self.va_log and self.va_log.timedelta:
            return op(dt, self.va_log.timedelta)
        return dt
    def convert_to_log_zone(self, dt):
        return self._convert_to_zone(dt, lambda d1, d2: d1 + d2)
    def convert_to_system_zone(self, dt):
        return self._convert_to_zone(dt, lambda d1, d2: d1 - d2)
    def get_regexes_for_sampling(self):
        if self.utterance_from_va and self.utterance_from_va.regexes:
            return [(regex.begin, regex.end) for regex in self.utterance_from_va.regexes]
        return []

class ConfigProxy:
    def __init__(self, config_json_path = None, schema_json_path = None):
        self.config = None
        if config_json_path and os_proxy.exists(config_json_path):
            self.config = Config(config_json_path, schema_json_path)
    def get_copy(self):
        import copy
        return copy.deepcopy(self)
    def get_vatf_branch_to_clone(self):
        if not self.config:
            return ""
        return self.config.get_vatf_branch_to_clone()
    def get_pathes_audio_files(self):
        if not self.config:
            return []
        return self.config.get_pathes_audio_files()
    def convert_to_log_zone(self, dt):
        if not self.config:
            return dt
        return self.convert_to_log_zone(dt)
    def convert_to_system_zone(self, dt):
        if not self.config:
            return dt
        return self.convert_to_system_zone(dt)
    def get_regexes_for_sampling(self):
        if not self.config:
            return []
        return self.config.get_regexes_for_sampling()

def _abs_path_to_schema():
    import pathlib
    path = pathlib.Path(__file__).parent.resolve()
    return os_proxy.join(path, "schemas/config.schema.json")

def load(config_json_path = "./config.json", schema_json_path = _abs_path_to_schema()):
    return ConfigProxy(config_json_path, schema_json_path)
