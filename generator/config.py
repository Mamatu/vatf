import abc
import os

import logging

from vatf.utils.config_loader import ConfigLoader

def get_pathes_to_audio_files():
    pass

def get_path_to_generated_suite():
    pass

def get_path_to_generated_test():
    pass

def get_relative_path_to_audio_files_in_test():
    pass

def get_absolute_path_to_audio_files_in_test():
    test_path = get_path_to_generated_test()
    audio_files_path = get_relative_path_to_audio_files_in_test()
    return os.path.join(test_path, audio_files_path)
