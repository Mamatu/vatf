def get_global_schema_path():
    from vatf.utils import os_proxy
    import pathlib
    path = pathlib.Path(__file__).parent.parent.resolve()
    return os_proxy.join(path, "schemas/config.schema.json")

def process_format(config_dict, format_dict):
    for k,v in config_dict.items():
        if isinstance(v, dict):
            process_format(v, format_dict)
        elif isinstance(v, str):
            v = v.format(**format_dict)
            config_dict[k] = v
    return config_dict
