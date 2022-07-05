from vatf import vatf_api

def _get_api():
    return vatf_api.get_api("mkdir")

def get_count(path):
    return _get_api().get_count(path)

def get_count_path(path):
    return _get_api().get_count_path(path)

def mkdir(path):
    _get_api().mkdir(path)

def mkdir_with_counter(path):
    _get_api().mkdir_with_counter(path)
