import os
import shutil
import sys
import uuid
from enum import Enum
from random import random
from random import randint

from vatf.generator import ctx
from vatf.generator import command as cmd

_rec_bg = None

def Rec():
    global _rec_bg
    filepath = ctx.Get().mkdir_incr("./recordings/session")
    rec_command = f"python vatf_utils/papy.py --recorder=gst --rec --dir $(cat {filepath})"
    _rec_bg = cmd.RunBg(rec_command, "SIGINT")
    return filepath

def Start():
    Rec()

def Stop():
    cmd.KillBg(_rec_bg)
