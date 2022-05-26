from vatf import vatf_api

def _get_api():
    return vatf_api.get_api("log_snapshot")

def start(log_path, shell_cmd, restart_timeout):
    _get_api().start(log_path, shell_cmd, restart_timeout)

def start_from_config():
    _get_api().start_from_config()