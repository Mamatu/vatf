import os
import shutil
import sys
import uuid
from enum import Enum
from random import random
from random import randint

from vatf.generator import ctx
from vatf.generator.core import context

import logging

class SamplingConfig:
    path_to_log : str
    path_to_recording : str
    path_to_recording_date : str
    start_regex : str
    end_regex : str
    from_line : int
    count : int
    path_to_search_lines : str
    path_to_search_start_date : str
    def __init__(self, config = None):
        self.path_to_log = None
        self.path_to_recording = None
        self.path_to_recording_date = None
        self.start_regex = None
        self.end_regex = None
        self.from_line = 0
        self.count = -1
        self.path_to_search_lines = None
        self.path_to_search_start_date = None
        if config and len(config.utterance_from_va.regexes) == 1:
            self.start_regex = config.utterance_from_va.regexes[0].begin
            self.end_regex = config.utterance_from_va.regexes[0].end

def RunWithConfig(config):
    assert(isinstance(config, SamplingConfig))
    samplerConfig = context.Context.SamplerConfig()
    samplerConfig.path_to_samples = "./samples/session"
    for k,v in config.__dict__.items():
        if k in samplerConfig.__dict__.keys():
            if isinstance(v, str):
                setattr(samplerConfig, k, f"\"{v}\"")
            elif v != None:
                setattr(samplerConfig, k, v)
    storage = ctx.Get().mkdir_incr(samplerConfig.path_to_samples)
    samplerConfig.path_to_samples = f"$(cat {storage})"
    ctx.Get().sampling(samplerConfig)
