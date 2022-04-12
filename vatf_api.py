from enum import Enum

from vatf.generator import player as gen_player
from vatf.executor import player as exec_player

class API_TYPE(Enum):
    EXECUTOR = 1,
    GENERATOR = 2

_apiType = API_TYPE.GENERATOR
_api = {API_TYPE.GENERATOR : gen_player, API_TYPE.EXECUTOR : exec_player}

def set_api_type(apiType):
    global _apiType
    _apiType = apiType

def get_api():
    return _api[_apiType]
