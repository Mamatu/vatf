def get_global_schema_path():
    from vatf.utils import os_proxy
    import pathlib
    path = pathlib.Path(__file__).parent.parent.resolve()
    return os_proxy.join(path, "schemas/config.schema.json")

def update_with_default_format(custom_format):
    if custom_format is None:
        custom_format = {}
    default_format = {}
    import datetime
    date = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    default_format["config_loading_time"] = date
    custom_format.update(default_format)
    return custom_format

def prepare_format_dict(data, custom_format = None):
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
    format_dict = update_with_default_format(format_dict)
    return format_dict

def process_format(config_dict, format_dict):
    format_dict = prepare_format_dict(config_dict, format_dict)
    for k,v in config_dict.items():
        if isinstance(v, dict):
            process_format(v, format_dict)
        elif isinstance(v, str):
            try:
                v = v.format(**format_dict)
                config_dict[k] = v
            except:
                pass
    return config_dict
