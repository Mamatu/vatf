from vatf import vatf_api

def _get_api():
    return vatf_api.get_api("shell")

def fg(command):
    _get_api().fg(command)

def bg(command):
    _get_api().bg(command)
