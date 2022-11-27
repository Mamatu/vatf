def get_global_schema_path():
    from vatf.utils import os_proxy
    import pathlib
    path = pathlib.Path(__file__).parent.parent.resolve()
    return os_proxy.join(path, "schemas/config.schema.json")

