__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import logging
import datetime
import os
import re

from vatf.utils import ac
from vatf.utils import utils

import vatf.utils

def _get_from_kwargs(attr, attr_in_config, **kwargs):
    attr_value = None
    if attr in kwargs:
        attr_value = kwargs[attr]
    else:
        from utils import config_handler
        config = config_handler.get_config(**kwargs)
        attr_value = config[attr_in_config]
    if attr_value is None:
        raise Exception(f"Cannot find no {attr} in kwargs or {attr_in_config} in config")
    return attr_value

def _get_timestamp_regex_from_kwargs(**kwargs):
    return _get_from_kwargs("timestamp_regex", "log_snapshot.timestamp_regex", **kwargs)

def _get_timestamp_format_from_kwargs(**kwargs):
    return _get_from_kwargs("timestamp_format", "log_snapshot.timestamp_format", **kwargs)

def _convert_pcm_to_ogg(recording_path, audioConfig):
    from vatf.utils import ffmpeg
    output_path = utils.get_temp_file()
    output_path = f"{output_path}.ogg"
    vatf.utils.ffmpeg.convert(recording_path, output_path, audioConfig)
    return output_path

def get_creation_date(path, timestamp_format, **kwargs):
    #timestamp_format = _get_timestamp_format_from_kwargs(**kwargs)
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    read_date_stat = lambda: utils.get_modification_date(path)
    try:
        with open(path, "tr") as f:
            content = f.read().rstrip()
            logging.info(f"Reading: {content}")
            return datetime.datetime.strptime(content, timestamp_format)
    except ValueError as vex:
        logging.info(f"Exception {str(vex)} during an attempt of reading {path}. Reads date stat")
        return read_date_stat()
    except BaseException as ex:
        logging.info(f"Cannot open {path} due to {ex} in text mode. Reads date stat")
        return read_date_stat()

def get_recording_start_date(path_to_recording, path_to_recording_date, timestamp_format):
    if path_to_recording_date:
        return get_creation_date(path_to_recording_date, timestamp_format = timestamp_format)
    if path_to_recording:
        return get_creation_date(path_to_recording, timestamp_format = timestamp_format)

def extract_sample(start_regex_timestamp, end_regex_timestamp, recording_start_timestamp, audioData, sr, samples_path, sample_format = "ogg"):
    logging.info(f"{extract_sample.__name__} sample : {start_regex_timestamp} {end_regex_timestamp} recordin start : {recording_start_timestamp}")
    if end_regex_timestamp is not None and recording_start_timestamp > end_regex_timestamp:
        return None
    start_timestamp = start_regex_timestamp - recording_start_timestamp
    end_timestamp = None if end_regex_timestamp is None else end_regex_timestamp - recording_start_timestamp
    start_timestamp = start_timestamp.total_seconds()
    end_timestamp = None if end_timestamp is None else end_timestamp.total_seconds()
    logging.info(f"Exctract time from recording {start_timestamp} {end_timestamp} sampling_rate {sr}")
    start_index = start_timestamp * sr
    end_index = None if end_timestamp is None else end_timestamp * sr
    logging.info(f"Exctract audio data from recording {start_index} {end_index} sampling_rate {sr}")
    audio_sample = None
    if end_index is None:
        audio_sample = audioData[int(start_index) :]
    else:
        audio_sample = audioData[int(start_index) : int(end_index)]
    sample_name = "sample_"
    sample_counter = utils.get_counter(samples_path, sample_name, sample_format) + 1
    sample_path = os.path.join(samples_path, f"{sample_name}{sample_counter}.{sample_format}")
    import soundfile as sf
    sf.write(sample_path, audio_sample, sr)
    logging.info(f"Write sample to {sample_path}")
    return sample_path

def extract_samples(recording_start_timestamp, regexes, recording_path, samples_path, timestamp_format, audioConfig = vatf.utils.ac.AudioConfig(vatf.utils.ac.Format.s16le, channels = 1, framerate = 44100), sample_format = "ogg", **kwargs):
    #timestamp_format = _get_timestamp_format_from_kwargs(**kwargs)
    import librosa
    audio = []
    sr = None
    try:
        audio, sr = librosa.load(recording_path, sr = None)
    except BaseException as ex:
        logging.warning(f"Exception {ex}. Try convert to ogg format...")
        filepath = _convert_pcm_to_ogg(recording_path, audioConfig)
        audio, sr = librosa.load(filepath, sr = None)
        os.remove(filepath)
    if len(audio) == 0:
        logging.error(f"Could not load data from {recording_path}")
        return
    sample_paths = []
    not_matched_samples_count = 0
    for start_end in regexes:
        start_timestmap = datetime.datetime.strptime(start_end[0].matched[0], timestamp_format)
        end_timestamp = None
        if start_end[1] is not None:
            end_timestamp = datetime.datetime.strptime(start_end[1].matched[0], timestamp_format)
        sample_path = extract_sample(start_timestmap, end_timestamp, recording_start_timestamp, audio, sr, samples_path, sample_format = sample_format)
        if sample_path != None:
            sample_paths.append(sample_path)
        else:
            not_matched_samples_count = not_matched_samples_count + 1
    logging.info(f"Extracted {len(sample_paths)} samples. {not_matched_samples_count} samples could not extract (not in recording)")
    return sample_paths

def find_start_end_regexes(path_to_log, start_regex, end_regex, from_line, max_count, timestamp_regex, **kwargs):
    #timestamp_regex = _get_timestamp_regex_from_kwargs(**kwargs)
    start_regexes = utils.grep_regex_in_line(filepath = path_to_log, grep_regex = start_regex, match_regex = timestamp_regex, maxCount = max_count)
    end_regexes = utils.grep_regex_in_line(filepath = path_to_log, grep_regex = end_regex, match_regex = timestamp_regex, maxCount = max_count)
    def get_end_regexes(idx):
        if idx >= len(end_regexes):
            return None
        return end_regexes[idx]
    regexes = [(start_regexes[i], get_end_regexes(i)) for i in range(0, len(start_regexes))]
    if from_line and from_line > 0:
        from_line = int(from_line)
        while regexes[0].line_number < from_line:
            regexes.pop(0)
    return regexes

def _checks_args(args):
    def mandatory(arg, path):
        if not (path and os.path.exists(path)):
            raise Exception(f"Mandatory {arg} {path} doesn't exist")
    def not_mandatory(arg, path):
        if path and not os.path.exists(path):
            raise Exception(f"Not existed {arg}: {path}")
    def mandatory_create_if_not_exist(arg, path):
        if not os.path.exists(path):
            os.makedirs(path)
    mandatory("{args.path_to_log=}", args.path_to_log)
    mandatory("{args.path_to_recording=}", args.path_to_recording)
    mandatory_create_if_not_exist("{args.path_to_samples=}", args.path_to_samples)
    not_mandatory("{args.path_to_recording_date=}", args.path_to_recording_date)

def process(args):
    _checks_args(args)
    start_date = get_recording_start_date(args.path_to_recording, args.path_to_recording_date, args.timestamp_format)
    #start_date = config.ConvertToLogZone(start_date)
    #if not args.regexes.begin and not args.end_regex:
    #    regexes = config.GetRegexesForSampling()
    #    args.start_regex = regexes[0][0]
    #    args.end_regex = regexes[0][1]
    #    if len(regexes) > 1:
    #        logging.error("Number of regexes > 1 is not supported. Only the first one will be used")
    if not (args.regexes.begin and args.regexes.end):
        raise Exception("Inproper pair of start and end regex. Please provide both as arguments in config")
    maxCount = -1
    #if args.count:
    #    maxCount = args.count
    #regexes = find_start_end_regexes(args.path_to_log, args.regexes.begin, args.regexes.end, args.from_line, maxCount)
    regexes = find_start_end_regexes(args.path_to_log, args.regexes.begin, args.regexes.end, 0, maxCount, args.timestamp_regex)
    #if args.path_to_search_lines:
    #if args.path_to_log:
    #    with open(args.lines_save_to, "w") as f:
    #        array = []
    #        for start_end in regexes:
    #            array.append(start_end[0].line_number)
    #            array.append(start_end[1].line_number)
    #        f.write("\n".join(array))
    sample_pathes = extract_samples(start_date, regexes, args.path_to_recording, args.path_to_samples, args.timestamp_format)
    logging.info(f"Created: {sample_pathes}")
