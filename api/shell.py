from vatf import vatf_api

def _get_api():
    return vatf_api.get_api("shell")

def fg(command):
    _get_api().fg(command)

def bg(command, shell = True):
    _get_api().bg(command, shell)

def kill(process):
    _get_api().kill(process)
