import logging
import inspect
import json
import jsonschema
from jsonschema import validate
import os

from vatf.utils import os_proxy

class Vatf:
    def __init__(self, data):
        vatf = data["vatf"]
        self.branch = vatf["branch"]
    @staticmethod
    def load(data):
        if not data or not "vatf" in data:
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
    def load(data):
        if not data or not "assets" in data:
            return None
        return Assets(data)

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
    def load(data):
        if data and 'utterance_from_va' in data:
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
    def load(data):
        if data and 'utterance_to_va' in data:
            return UtteranceToVA(data)
        return None

class Command():
    def __init__(self, data):
        data = data["command"]
        self.shell = data["shell"]
        self.restart_timeout = int(data["restart_timeout"])
    @staticmethod
    def load(data):
        if "command" in data:
            return Command(data)
        return None

class VaLog:
    def __init__(self, data):
        import datetime
        va_log = data["va_log"]
        self.path = va_log["path"]
        self.timedelta = datetime.timedelta(**va_log["timedelta"])
        self.date_regex = va_log["date_regex"]
        self.date_format = va_log["date_format"]
        self.command = Command.load(va_log)
    @staticmethod
    def load(data):
        if data and 'va_log' in data:
            return VaLog(data)
        return None

class Format:
    def __init__(self, data):
        _format = data['format']
        for item in _format:
            setattr(self, item['key'], item['value'])
    @staticmethod
    def load(data):
        if data and 'format' in data:
            return Format(data)
        return None

class Config:
    def __init__(self, data = None):
        self.vatf = Vatf.load(data)
        self.assets = Assets.load(data)
        self.va_log = VaLog.load(data)
        self.utterance_from_va = UtteranceFromVA.load(data)
        self.utterance_to_va = UtteranceToVA.load(data)
        if self.assets and self.assets.audio and self.assets.audio.path:
            self.searched_audio_files_pathes = self.assets.audio.path
        else:
            self.searched_audio_files_pathes = None
        self.format = Format.load(data)
    def _get_not_none(self, orig, other):
        xor = lambda a,b: (a and not b) or (not a and b)
        outcome = orig
        if not xor(orig, other):
            if orig:
                raise Exception(f"{orig.__name__} cannot be merged")
            if other:
                raise Exception(f"{other.__name__} cannot be merged")
        else:
            if other:
                outcome = other
        return outcome
    def _merge(self, orig, other):
        outcome = orig
        for value, key in inspect.getmembers(other):
            setattr(outcome, value, key)
    def __add__(self, other):
        outcome = Config()
        outcome.vatf = self._get_not_none(self.vatf, other.vatf)
        outcome.assets = self._get_not_none(self.assets, other.assets)
        outcome.va_log = self._get_not_none(self.va_log, other.va_log)
        outcome.utterance_from_va = self._get_not_none(self.utterance_from_va, other.utterance_from_va)
        outcome.utterance_to_va = self._get_not_none(self.utterance_to_va, other.utterance_to_va)
        #outcome.format = self._merge(self.format, other.format)
        return outcome
    @staticmethod
    def load(config_json_path = None, schema_json_path = None):
        with open(config_json_path) as f:
            logging.debug(f"Reads {config_json_path}")
            data = json.load(f)
            if schema_json_path:
                with open(schema_json_path) as schema:
                    logging.debug(f"Validation {config_json_path} by use schema {schema.name}")
                    validate(data, schema=json.load(schema))
        return Config(data)

def _abs_path_to_schema():
    import pathlib
    path = pathlib.Path(__file__).parent.parent.resolve()
    return os_proxy.join(path, "schemas/config.schema.json")

def load(config_json_path = "./config.json", schema_json_path = _abs_path_to_schema()):
    return Config.load(config_json_path, schema_json_path)
