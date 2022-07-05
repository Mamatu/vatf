_configs = None

class _Configs:
    def __init__(self, configs = None):
        if isinstance(configs, str):
            configs = [configs]
        self.configs = []
        if configs:
            for config in configs:
                self.load(config)
    def load(self, path):
        from vatf.utils import config_loader
        self.configs.append(config_loader.load(path))
    def get(self, var, raiseIfNotFound = True):
        from vatf.utils import config_loader
        for config in self.configs:
            attr = config_loader.get(config, var, False)
            if attr:
                return attr
        if raiseIfNotFound:
            raise AttributeError(f"Attr {var} not found in config")
        return None

def init_configs(config_pathes):
    global _configs
    _configs = _Configs(config_pathes)
    return _configs

def reset_configs():
    global _configs
    _configs = None

def get():
    return _configs

def _handle_global_config(config_vars, custom_format):
    global _configs
    if _configs is None:
        raise Exception("global config does not exist")
    return handle_config(config_vars, _configs, custom_format)

def _handle_config(config_vars, config, custom_format, callback = None):
    _dict = {}
    for attr in config_vars:
        value = config.get(attr)
        if callback: callback(attr, value)
        if custom_format:
            value = value.format(**custom_format)
        _dict[attr] = value 
    return _dict

def _handle_config_path(config_vars, path, custom_format):
    from vatf.utils import config_loader
    config = config_loader.load(path, custom_format = custom_format)
    return _handle_config(config_vars, config, custom_format = custom_format)

def _handle_config_attrs(config_vars, kw_config_vars, custom_format):
    def callback(k, v):
        if v is None:
            raise Exception("Attr {k} is None")
    return _handle_config(config_vars, kw_config_vars, custom_format = custom_format, callback = callback)

def handle(config_vars, custom_format = None, **kwargs):
    is_config_path = "config_path" in kwargs.keys()
    is_config = "config" in kwargs.keys()
    is_config_vars = "config_attrs" in kwargs.keys()
    true_list = [is_config_path, is_config, is_config_vars]
    true_list = [x for x in true_list if x]
    if len(true_list) > 1:
        raise Exception("kwargs can contain only one: config, config_path or config attrs")
    _dict = {}
    if is_config_vars:
        kw_config_vars = kwargs["config_attrs"]
        return _handle_config_attrs(config_vars, kw_config_vars, custom_format = custom_format)
    if is_config_path:
        config_path = kwargs["config_path"]
        return _handle_config_path(config_vars, config_path, custom_format = custom_format)
    if is_config:
        config = kwargs["config"]
        return _handle_config(config_vars, config, custom_format = custom_format)
    if len(true_list) == 0:
        return _handle_global_config(config_vars, custom_format = custom_format)
