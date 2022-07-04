import logging

import shutil
import sys
import uuid
from enum import Enum
import random

from vatf.generator import gen_tests
from vatf.utils import os_proxy

def _play_audio(path):
    gen_tests.create_call("player", "play_audio", path = path)

def get_random_audio_files(path, count = 1):
    dirs = [path]
    audiofiles = []
    files = []
    for c in range(count):
        for d in dirs:
            ls = os_proxy.listdir(d)
            for l in ls:
                dl = os_proxy.join(d, l)
                if os_proxy.isfile(dl):
                    files.append(l)
    if len(files) == 0:
        raise Exception("None files in dir")
    for c in range(count):
        idx = random.randint(0, len(files) - 1)
        audiofiles.append(files[idx])
    return audiofiles

def _get_all_file_pathes(pathes, audio_file):
    audio_file_pathes = []
    for p in pathes:
        audio_file_path = os_proxy.join(p, audio_file)
        if os_proxy.exists(audio_file_path):
            audio_file_pathes.append(audio_file_path)
    return audio_file_pathes

def _get_audio_file_path(config, audio_file):
    pathes = config.get_pathes_to_audio_files_in_system()
    if len(pathes) == 0:
        raise Exception(f"Lack of audio files pathes in system")
    audio_file_pathes = _get_all_file_pathes(pathes, audio_file)
    if len(audio_file_pathes) == 0:
        raise Exception(f"Audio file {audio_file} doesn't exist in pathes: {pathes}")
    return audio_file_pathes[0]

def play_audio(audiofile_id, find_in_audio_files_path = True):
    logging.debug(f"PlayAudio: {audiofile_id} {find_in_audio_files_path}")
    audiofile_path = _get_audio_file_path(config, audiofile_id)
    abs_path = config.get_absolute_path_to_audio_files_in_test()
    shutil.copyfile(audiofile_path, os_proxy.join(abs_path, os_proxy.basename(audiofile_path)))
    logging.debug(f"copy: {audiofile_path} -> {abs_path}")
    rel_path = config.get_relative_path_to_audio_files_in_test()
    audiofile_id = os_proxy.basename(audiofile_id)
    logging.debug(f"play: {audiofile_id} {rel_path}")
    _play_audio(os_proxy.join(rel_path, audiofile_id))

def play_random_audio(audiofiles = None, count = 1):
    if not audiofiles:
        audiofiles = get_random_audio_files(count)
    else:
        audiofiles = [audiofiles[random.randint(0, len(audiofiles) - 1)] for idx in range(count)]
    for audiofile in audiofiles:
        play_audio(audiofile)
