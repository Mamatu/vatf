import os
import disutils
import logging
import hashlib
import shutil

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def exists(path):
    return os.path.exists(path)

def remove(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def copy(src, dst):
    distutils.dir_util.copy_tree(src, dst)

def open_to_write(path):
    return open(path, "w")

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
