import logging

import os
import shutil
import sys
import uuid
from enum import Enum
import random

from vatf.generator import config, gen_core

def _play_audio(path):
    gen_core.generate("play_audio", path = path)

def get_random_audio_files(count = 1):
    dirs = config.get_pathes_to_audio_files()
    audiofiles = []
    files = []
    for c in range(count):
        for d in dirs:
            ls = os.listdir(d)
            for l in ls:
                dl = os.path.join(d, l)
                if os.path.isfile(dl):
                    files.append(l)
    if len(files) == 0:
        raise Exception("None files in dir")
    for c in range(count):
        idx = random.randint(0, len(files) - 1)
        audiofiles.append(files[idx])
    return audiofiles

def play_audio(audiofile_path, find_in_audio_files_path = True):
    logging.debug(f"PlayAudio: {audiofile_path} {find_in_audio_files_path}")
    if find_in_audio_files_path:
        existed = ctx.Get().getExistedAudioFilesPathes(audiofile_path)
        if len(existed) == 0:
            all_searched_pathes = ctx.Get().getAudioFilesPathes()
            raise Exception(f"Cannot find any audiofile in searched pathes: {all_searched_pathes}")
        logging.debug(f"Existed pathes {existed}")
        audiofile_path = existed[0]
    dst = os.path.join(ctx.Get().getConfig().abs_audio_files_path_in_test, os.path.basename(audiofile_path))
    logging.debug(f"copy: {audiofile_path} -> {dst}")
    shutil.copyfile(audiofile_path, dst)
    rel_path = config.get_relative_path_to_audio_files_in_test()
    audiofile_path = os.path.basename(audiofile_path)
    logging.debug(f"play: {audiofile_path} {rel_path}")
    _play_audio(os.path.join(rel_path, audiofile_path))

def play_random_audio(count = 1):
    audiofiles = get_random_audio_files(count)
    for audiofile in audiofiles:
        play_audio(audiofile)
