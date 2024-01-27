__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

def get_global_schema_path():
    from vatf.utils import os_proxy
    import pathlib
    path = pathlib.Path(__file__).parent.parent.resolve()
    return os_proxy.join(path, "schemas/config.schema.json")

def update_with_default_format(custom_format, **kwargs):
    if custom_format is None:
        custom_format = {}
    default_format = {}
    if not "config_loading_time" in kwargs:
        raise Exception("Lack of config_loading_time in kwargs")
    date = kwargs["config_loading_time"]
    default_format["config_loading_time"] = date
    custom_format.update(default_format)
    return custom_format

def prepare_format_dict(data, custom_format = None, **kwargs):
    def make_dict(data_format):
        _dict = {}
        for kv in data_format:
            _dict[kv.key] = kv.value
        return _dict
    format_dict = {}
    if "format" in data and data["format"]:
        format_dict.update(data["format"])
    if custom_format:
        format_dict.update(custom_format)
    format_dict = update_with_default_format(format_dict, **kwargs)
    return format_dict

def process_format(config_dict, format_dict, **kwargs):
    format_dict = prepare_format_dict(config_dict, format_dict, **kwargs)
    for k,v in config_dict.items():
        if isinstance(v, dict):
            process_format(v, format_dict, **kwargs)
        elif isinstance(v, list):
            for i in range(len(v)):
                if isinstance(v[i], dict):
                    process_format(v[i], format_dict, **kwargs)
                elif isinstance(v, str):
                    try:
                        v = v.format(**format_dict)
                        config_dict[k] = v
                    except:
                        pass
        elif isinstance(v, str):
            try:
                v = v.format(**format_dict)
                config_dict[k] = v
            except:
                pass
    return config_dict

def convert_dict_to_timedelta(timedelta):
    if isinstance(timedelta, dict):
        args = {}
        def get_key(key):
            v = None
            try:
                v = timedelta[key]
            except KeyError:
                pass
            if v: args[key] = v
            else: args[key] = 0
        get_key("days")
        get_key("seconds")
        get_key("microseconds")
        get_key("milliseconds")
        get_key("minutes")
        get_key("hours")
        get_key("weeks")
        import datetime
        return datetime.timedelta(**args)
    return timedelta
