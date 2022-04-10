import command
import mkdir

from vatf.generator import ctx

_logger_bg = None

def Start(path_to_dir_pattern):
    global _logger_bg
    if not ctx.Get().config:
        raise Exception("Config is not availabe")
    if not ctx.Get().config.va_log:
        raise Exception("Config doesn't contain va_log section")
    if not ctx.Get().config.va_log.path:
        raise Exception("Config doesn't contain va_log.path string")
    path_to_log = ctx.Get().config.va_log.path
    path_to_dir = mkdir.MkdirIncr(path_to_dir_pattern)
    _logger_bg = command.RunBg(f"python vatf_executor/main.py logger --path_to_input_log {path_to_log} --path_to_output_dir $(cat {path_to_dir}) --output_file_name session.log", "SIGINT")

def Stop():
    global _logger_bg
    command.KillBg(_logger_bg)
