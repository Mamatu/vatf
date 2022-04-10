import json
import jsonschema
from jsonschema import validate
import logging
import os

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
        self.searched_audio_files_pathes = ""
        self.data = None
        if config_json_path:
            with open(config_json_path) as f:
                logging.debug(f"Reads {config_json_path}")
                data = json.load(f)
                self.data = data
                if schema_json_path:
                    with open(schema_json_path) as schema:
                        logging.debug(f"Validation {config_json_path} by use schema {schema.name}")
                        validate(data, schema=json.load(schema))
                self.assets = Assets(data)
                self.va_log = VaLog(data)
                self.utterance_from_va = UtteranceFromVA.create(data)
                self.utterance_to_va = UtteranceToVA.create(data)
                self.searched_audio_files_pathes = self.assets.audio.path

_config = None

def LoadConfig(config_json_path = "./config.json", schema_json_path = None):
    global _config
    if not _config:
        if os.path.exists(config_json_path):
            _config = Config(config_json_path, schema_json_path)
        else:
            logging.warning("LoadConfig cannot find ./config.py. It supposes that it is expectional")

def _convert_to_zone(dt, config, op):
    if not config:
        global _config
        LoadConfig()
        config = _config
    if config and config.va_log and config.va_log.timedelta:
        return op(dt, config.va_log.timedelta)
    return dt

def ConvertToLogZone(dt, config = None):
    return _convert_to_zone(dt, config, lambda d1, d2: d1 + d2)

def ConvertToSystemZone(dt, config = None):
    return _convert_to_zone(dt, config, lambda d1, d2: d1 - d2)

def GetRegexesForSampling(config = None):
    if not config:
        global _config
        LoadConfig()
        config = _config
    if config and config.utterance_from_va and config.utterance_from_va.regexes:
        return [(regex.begin, regex.end) for regex in config.utterance_from_va.regexes]
    return []
