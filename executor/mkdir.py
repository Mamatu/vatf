import os
import re

from vatf_utils import utils
import logging

def Mkdir(path):
    os.makedirs(path)

def MkdirByCounter(dirpath):
    top = os.path.basename(dirpath)
    dir = os.path.dirname(dirpath)
    counter = utils.get_counter(dir, top) + 1
    path = f"{os.path.join(dir, top)}_{counter}/"
    os.makedirs(path)
    logging.info(f"{MkdirByCounter.__name__}: {path}")
    return path

def OutputToSave(path_to_save, txt):
    logging.info(f"{OutputToSave.__name__}: {txt} into {path_to_save}")
    if txt == None:
        txt = "None"
    with open(path_to_save, "w") as of:
        of.write(txt)

def main(args):
    path = None
    if args.path_to_counter:
        path = MkdirByCounter(args.path_to_counter)
    if args.output_save_to:
        OutputToSave(args.output_save_to, path)
