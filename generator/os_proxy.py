import os
import logging

class _FileProxy:
    def __init__(self, path, flag):
        self.file = open(path, flag)
    def write(self, data):
        self.file.write(data)
    def writeln(self, data):
        self.file.write(f"{data}\n")

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def open_to_write(path):
    f = _FileProxy(path, "w")
    return f

def write_to_file(handler, data):
    if isinstance(handler, str):
        handler = open_to_write(handler)
    if not isinstance(handler, _FileProxy):
        raise Exception(f"Invalid handler type")
    handler.write(data)

def writeln_to_file(handler, data):
    if isinstance(handler, str):
        handler = open_to_write(handler)
    if not isinstance(handler, _FileProxy):
        raise Exception(f"Invalid handler type")
    handler.writenl(data)
