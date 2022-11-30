from deprecation import deprecated

_global_config_pathes = None

class NoConfigException(Exception):
    pass

class NoAttrConfigException(Exception):
    pass

class _Global:
    def __init__(self):
        self.config_pathes = None
        self.custom_format = None
    def exist(self):
        return self.config_pathes != None

__global_config = _Global()

class _Configs:
    def __init__(self, pathes = None, custom_format = None):
        if isinstance(pathes, str):
            pathes = [pathes]
        if pathes:
            self.data = self.load(pathes, custom_format)
    def load(self, pathes, custom_format):
        data = {}
        from vatf.utils import config_loader
        for path in pathes:
            config = config_loader.load(path, custom_format = custom_format)
            data.update(config)
        return data
    def get(self, var, raiseIfNotFound = True):
        from vatf.utils import config_loader
        if var in self.data:
            return self.data[var]
        if raiseIfNotFound:
            raise NoAttrConfigException(f"Attr {var} not found in config")
        return None

class Config:
    class _Wrapper:
        def __init__(self, attr):
            self.attr = attr
        def __getattr__(self, attr):
            if isinstance(self.attr, dict):
                if attr in self.attr:
                    if isinstance(self.attr[attr], dict):
                        return Config._Wrapper(self.attr[attr])
                    elif isinstance(self.attr[attr], list):
                        wrappers = [Config._Wrapper(a) for a in self.attr[attr]]
                        return wrappers
                    else:
                        return self.attr[attr]
                else:
                    raise AttributeError
        def __getitem__(self, k):
            array = k.split(".")
            attr = self.attr
            for a in array:
                attr = attr[a]
            return attr
    def make_format(self, custom_format = None):
        if custom_format is None:
            return self.data
        from vatf_utils import config_common
        return config_common.process_format(self.data, custom_format)
    def __init__(self, data, custom_format = None):
        import copy
        self.__data = copy.deepcopy(data)
        self.data = data
        self.data = self.make_format(custom_format)
        self.data = Config._Wrapper(self.data)
    def get_raw_data(self):
        return self.__data
    def __getattr__(self, attr):
        return getattr(self.data, attr)
    def __getitem__(self, item):
         return self.data[item]

def init_configs(config_pathes, custom_format = None):
    global __global_config
    __global_config.config_pathes = config_pathes
    __global_config.custom_format = custom_format

def reset_configs():
    global _global_config
    _global_config = _Global()

def get():
    return _global_config_pathes

def _handle_global_config(config_vars, custom_format):
    global __global_config
    if not __global_config.exist():
        raise NoConfigException("no config is existing")
    from utils import config_loader
    data = config_loader.load(__global_config.config_pathes, custom_format = __global_config.custom_format, returnRawDict = True)
    return Config(data)

def _get_global_config(custom_format):
    global _global_config_pathes
    if _global_config_pathes is None:
        raise NoConfigException("no config is existing")
    return _get_config(_global_config_pathes, custom_format)

def _handle_config(config_vars, config, custom_format, callback = None):
    _dict = {}
    for attr in config_vars:
        value = config.get(attr)
        if callback: callback(attr, value)
        if custom_format:
            value = value.format(**custom_format)
        _dict[attr] = value 
    return _dict

def _get_config(config, custom_format, callback = None):
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
            raise NoAttrConfigException("Attr {k} is None")
    return _handle_config(config_vars, kw_config_vars, custom_format = custom_format, callback = callback)

def _get_config_attrs(kw_config_vars, custom_format):
    def callback(k, v):
        if v is None:
            raise NoAttrConfigException("Attr {k} is None")
    return _get_config(kw_config_vars, custom_format = custom_format, callback = callback)

def _get_handle_config_dict(kw_config_dict, custom_format):
    return Config(kw_config_dict, custom_format)

def _get_handle_config_path(config_path, custom_format):
    from utils import config_loader
    data = config_loader.load(config_path, returnRawDict = True)
    return Config(data, custom_format)

def _get_handle_config(config, custom_format):
    raw_data = config.get_raw_data()
    return Config(raw_data, custom_format)

def _get_handle_global_config(custom_format):
    global __global_config
    if not __global_config.exist():
        raise NoConfigException("no config is existing")
    from utils import config_loader
    data = config_loader.load(__global_config.config_pathes, custom_format = __global_config.custom_format, returnRawDict = True)
    return Config(data)

def get_config(custom_format = None, **kwargs):
    is_config_path = "config_path" in kwargs.keys()
    is_config = "config" in kwargs.keys() and isinstance(kwargs["config"], Config)
    is_config_dict = "config" in kwargs.keys() and isinstance(kwargs["config"], dict)
    is_config_dict = is_config_dict or "config_attrs" in kwargs.keys() # support for decprecated config_attrs
    true_list = [is_config_path, is_config, is_config_dict]
    true_list = [x for x in true_list if x]
    if len(true_list) > 1:
        raise Exception("kwargs can contain only one: config, config_path or config attrs")
    if is_config_dict:
        kw_config_dict = kwargs["config"]
        return _get_handle_config_dict(kw_config_dict, custom_format = custom_format)
    if is_config_path:
        config_path = kwargs["config_path"]
        return _get_handle_config_path(config_path, custom_format = custom_format)
    if is_config:
        config = kwargs["config"]
        return _get_handle_config(config, custom_format = custom_format)
    if len(true_list) == 0:
        return _get_handle_global_config(custom_format = custom_format)

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

def has_var(config_var, custom_format = None, **kwargs):
    try:
        var = get_var(config_var, custom_format, **kwargs)
        return var is not None
    except:
        return False

def get_vars(config_vars, custom_format = None, **kwargs):
    return handle(config_vars, custom_format, **kwargs)

def get_var(config_var, custom_format = None, **kwargs):
    if not isinstance(config_var, str):
        raise Exception("config_var must be singe key")
    output = get_vars([config_var], custom_format, **kwargs)
    return output[config_var]
