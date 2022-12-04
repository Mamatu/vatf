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

class Config:
    class _Wrapper:
        def __init__(self, attr):
            self.attr = attr
            if isinstance(self.attr, dict):
                keys = [k for k in self.attr.keys()]
                for key in keys:
                    if isinstance(key, str):
                        key_splitted = key.split(".")
                        if len(key_splitted) > 1:
                            value = self.attr[key]
                            _attr = self.attr
                            while len(key_splitted) > 1:
                                k_ = key_splitted.pop(0)
                                v_ = key_splitted[0]
                                if k_ not in _attr:
                                    d = {v_ : {}}
                                    _attr[k_] = d
                                else:
                                    _attr[k_][v_] = {}
                                _attr = _attr[k_]
                            _attr[key_splitted.pop(0)] = value
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
                    raise AttributeError(f"Attribute error: {attr}")
        def __getitem__(self, k):
            array = k.split(".")
            attr = self.attr
            for a in array:
                attr = attr[a]
            return attr
    def make_format(self, data, custom_format = None):
        from vatf.utils import config_common
        return config_common.process_format(data, custom_format)
    def __init__(self, data, custom_format = None):
        if isinstance(data, Config):
            data = data.get_raw_data_copy()
        import copy
        self.__data = copy.deepcopy(data)
        self.data = copy.deepcopy(data)
        self.data = self.make_format(self.data, custom_format)
    def get_raw_data(self):
        return self.__data
    def get_raw_data_copy(self):
        import copy
        return copy.deepcopy(self.get_raw_data())
    def __getattr__(self, attr):
        return getattr(Config._Wrapper(self.data), attr)
    def __getitem__(self, item):
        _data = Config._Wrapper(self.data)
        if isinstance(item, str):
            item = item.split(".")
            if len(item) == 1:
                return _data[item[0]]
            else:
                data = _data
                for i in item:
                    data = data[i]
                return data
    def get(self, item, raiseIfNotFound = True):
        try:
            return self[item]
        except KeyError as ke:
            return None

def init_configs(config_pathes, custom_format = None):
    global __global_config
    __global_config.config_pathes = config_pathes
    __global_config.custom_format = custom_format

def reset_configs():
    global _global_config
    _global_config = _Global()

def get():
    return _global_config_pathes

def _handle_global_config(custom_format):
    global __global_config
    if not __global_config.exist():
        raise NoConfigException("no config is existing")
    from vatf.utils import config_loader
    format_dict = {}
    if __global_config.custom_format:
        format_dict.update(__global_config.custom_format)
    if custom_format:
        format_dict.update(custom_format)
    data = config_loader.load(__global_config.config_pathes)
    return Config(data, custom_format = format_dict)

def _handle_config(config, custom_format):
    return Config(config, custom_format)

def _handle_config_path(config_path, custom_format):
    from vatf.utils import config_loader
    data = config_loader.load(config_path)
    return Config(data, custom_format)

def _handle_config_dict(kw_config_dict, custom_format):
    return Config(kw_config_dict, custom_format)

def get_config(custom_format = None, **kwargs):
    is_config_path = "config_path" in kwargs.keys()
    is_config = "config" in kwargs.keys() and isinstance(kwargs["config"], Config)
    is_config_dict1 = "config" in kwargs.keys() and isinstance(kwargs["config"], dict)
    is_config_dict2 = "config_attrs" in kwargs.keys() # support for decprecated config_attrs
    is_config_dict3 = "config_dict" in kwargs.keys() # support for extra config_dict
    config_list = [is_config_path, is_config, is_config_dict1, is_config_dict2, is_config_dict3]
    true_list = [x for x in config_list if x]
    if len(true_list) > 1:
        raise Exception(f"kwargs can contain only one: config, config_path or config_attrs. It has: {config_list}")
    is_config_dict = is_config_dict1 or is_config_dict2 or is_config_dict3
    if is_config_dict:
        cd_labels = ["config", "config_attrs", "config_dict"]
        def get_label():
            for l in cd_labels:
                if l in kwargs:
                    return l
            return None
        kw_config_dict = kwargs[get_label()]
        return _handle_config_dict(kw_config_dict, custom_format = custom_format)
    if is_config_path:
        config_path = kwargs["config_path"]
        return _handle_config_path(config_path, custom_format = custom_format)
    if is_config:
        config = kwargs["config"]
        return _handle_config(config, custom_format = custom_format)
    if len(true_list) == 0:
        return _handle_global_config(custom_format = custom_format)

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
        return _handle_config_dict(kw_config_vars, custom_format = custom_format)
    if is_config_path:
        config_path = kwargs["config_path"]
        return _handle_config_path(config_path, custom_format = custom_format)
    if is_config:
        config = kwargs["config"]
        return _handle_config(config, custom_format = custom_format)
    if len(true_list) == 0:
        return _handle_global_config(custom_format = custom_format)

def has_var(config_var, custom_format = None, **kwargs):
    try:
        config = get_config(custom_format, **kwargs)
        var = config.get(config_var)
        return var is not None
    except Exception as ex:
        print(f"kex {ex}")
        return False

def get_vars(config_vars, custom_format = None, **kwargs):
    return handle(config_vars, custom_format, **kwargs)

def get_var(config_var, custom_format = None, **kwargs):
    if not isinstance(config_var, str):
        raise Exception("config_var must be singe key")
    output = get_vars([config_var], custom_format, **kwargs)
    return output[config_var]
