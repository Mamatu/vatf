import os
import logging
import hashlib
import shutil

from vatf.utils import utils

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def exists(path):
    return os.path.exists(path)

def remove(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            raise Exception(f"Path {path} is not directory or file")

def copy(src, dst):
    shutil.copytree(src, dst, dirs_exist_ok=True)

def open_to_write(path):
    return open(path, "w")

def open_to_read(path):
    return open(path, "r")

def writeln_to_file(handler, data):
    write_to_file(handler, f"{data}\n")

def write_to_file(handler, data):
    from io import TextIOWrapper
    if isinstance(handler, str):
        handler = open_to_write(handler)
    if not isinstance(handler, TextIOWrapper):
        raise Exception(f"Invalid handler type")
    handler.write(data)

def dirname(path):
    return os.path.dirname(path)

def basename(path):
    return os.path.basename(path)

def join(path, *pathes):
    return os.path.join(path, *pathes)

def isfile(path):
    return os.path.isfile(path)

def listdir(path):
    return os.listdir(path)

def md5sum(filepath):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def create_tmp_file(mode, data = None, path = None):
    utils.print_func_info()
    file = None
    if path is None:
        file = utils.get_tmp_file(mode = mode)
    else:
        file = open(path, mode = mode)
    if data:
        file.write(data)
    file.flush()
    return file

def remove_file(path):
    os.remove(path)
