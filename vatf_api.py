from enum import Enum

from vatf.generator import player as gen_player
from vatf.executor import player as exec_player

from vatf.generator import sleep as gen_sleep
from vatf.executor import sleep as exec_sleep

from vatf.generator import shell as gen_shell
from vatf.executor import shell as exec_shell

from vatf.generator import shell as gen_mkdir
from vatf.executor import shell as exec_mkdir

class API_TYPE(Enum):
    EXECUTOR = 1,
    GENERATOR = 2

_apiType = API_TYPE.GENERATOR
_player_api = {API_TYPE.GENERATOR : gen_player, API_TYPE.EXECUTOR : exec_player}
_sleep_api = {API_TYPE.GENERATOR : gen_sleep, API_TYPE.EXECUTOR : exec_sleep}
_shell_api = {API_TYPE.GENERATOR : gen_shell, API_TYPE.EXECUTOR : exec_shell}
_mkdir_api = {API_TYPE.GENERATOR : gen_mkdir, API_TYPE.EXECUTOR : exec_mkdir}

_modules = {"player" : _player_api, "sleep" : _sleep_api, "shell" : _shell_api, "mkdir" : _mkdir_api}

def set_api_type(apiType):
    global _apiType
    _apiType = apiType

def get_api(module):
    if not module in _modules:
        raise Exception(f"Module {module} was not registered")
    return _modules[module][_apiType]
