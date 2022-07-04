class Configs:
    def __init__(self, configs = None):
        self.configs = []
        if configs:
            for config in configs:
                self.load(config)
    def load(self, path):
        from vatf.utils import config_loader
        self.configs.appends(config_loader.load(path))
    def get(self, var, raiseIfNotFound = True):
        from vatf.utils import config_loader
        for config in configs:
            attr = config_loader.get(config, var, False)
            if attr:
                return attr
        if raiseIfNotFound:
            raise AttributeError(f"Attr {var} not found in config")
        return None

_configs = None

def init_configs(configs):
    _configs = Configs(configs)
    return _configs

def get():
    return _configs
