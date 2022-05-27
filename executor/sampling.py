import logging
import datetime
import os
import re

from vatf.utils import ac
from vatf.utils import utils
from vatf.utils import config

import vatf.utils

DATE_REGEX = utils.DATE_REGEX
DATE_FORMAT = utils.DATE_FORMAT

TIMESTAMP_REGEX = utils.TIMESTAMP_REGEX
TIMESTAMP_FORMAT = utils.TIMESTAMP_FORMAT

def get_creation_date(path):
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    read_date_stat = lambda: utils.get_modification_date(path)
    try:
        with open(path, "tr") as f:
            content = f.read().rstrip()
            logging.info(f"Reading: {content}")
            return datetime.datetime.strptime(content, utils.DATE_FORMAT)
    except ValueError as vex:
        logging.info(f"Exception {str(vex)} during an attempt of reading {path}. Reads date stat")
        return read_date_stat()
    except BaseException as ex:
        logging.info(f"Cannot open {path} due to {ex} in text mode. Reads date stat")
        return read_date_stat()

def GetRecordingStartDate(path_to_recording, path_to_recording_date):
    if path_to_recording_date:
        return get_creation_date(path_to_recording_date)
    if path_to_recording:
        return get_creation_date(path_to_recording)

def ExctractSample(start_regex_timestamp, end_regex_timestamp, recording_start_timestamp, audioData, sr, samples_path, sample_format = "ogg"):
    logging.info(f"{ExctractSample.__name__} sample : {start_regex_timestamp} {end_regex_timestamp} recordin start : {recording_start_timestamp}")
    if recording_start_timestamp > end_regex_timestamp:
        return None
    start_timestamp = start_regex_timestamp - recording_start_timestamp
    end_timestamp = end_regex_timestamp - recording_start_timestamp
    start_timestamp = start_timestamp.total_seconds()
    end_timestamp = end_timestamp.total_seconds()
    logging.info(f"Exctract time from recording {start_timestamp} {end_timestamp} sampling_rate {sr}")
    start_index = start_timestamp * sr
    end_index = end_timestamp * sr
    logging.info(f"Exctract audio data from recording {start_index} {end_index} sampling_rate {sr}")
    audio_sample = audioData[int(start_index) : int(end_index)]
    sample_name = "sample_"
    sample_counter = utils.get_counter(samples_path, sample_name, sample_format) + 1
    sample_path = os.path.join(samples_path, f"{sample_name}{sample_counter}.{sample_format}")
    import soundfile as sf
    sf.write(sample_path, audio_sample, sr)
    logging.info(f"Write sample to {sample_path}")
    return sample_path

def _convert_pcm_to_ogg(recording_path, audioConfig):
    from vatf.utils import ffmpeg
    output_path = utils.get_temp_filepath()
    output_path = f"{output_path}.ogg"
    vatf.utils.ffmpeg.convert(recording_path, output_path, audioConfig)
    return output_path

def ExtractSamples(recording_start_timestamp, regexes, recording_path, samples_path, audioConfig = vatf.utils.ac.AudioConfig(vatf.utils.ac.Format.s16le, channels = 1, framerate = 44100), sample_format = "ogg"):
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
        start_timestmap = datetime.datetime.strptime(start_end[0].matched[0], utils.DATE_FORMAT)
        end_timestamp = datetime.datetime.strptime(start_end[1].matched[0], utils.DATE_FORMAT)
        sample_path = ExctractSample(start_timestmap, end_timestamp, recording_start_timestamp, audio, sr, samples_path, sample_format = sample_format)
        if sample_path != None:
            sample_paths.append(sample_path)
        else:
            not_matched_samples_count = not_matched_samples_count + 1
    logging.info(f"Extracted {len(sample_paths)} samples. {not_matched_samples_count} samples could not extract (not in recording)")
    return sample_paths

def FindStartEndRegexes(path_to_log, start_regex, end_regex, from_line, max_count):
    start_regexes = utils.grep_regex_in_line(filepath = path_to_log, grep_regex = start_regex, match_regex = utils.DATE_REGEX, maxCount = max_count)
    end_regexes = utils.grep_regex_in_line(filepath = path_to_log, grep_regex = end_regex, match_regex = utils.DATE_REGEX, maxCount = max_count)
    regexes = [(start_regexes[i], end_regexes[i]) for i in range(0, len(start_regexes))]
    if from_line and from_line > 0:
        from_line = int(from_line)
        while regexes[0].line_number < from_line:
            regexes.pop(0)
    return regexes

def _checks_args(args):
    def mandatory(arg, path):
        if not (path and os.path.exists(path)):
            raise Exception(f"Mandatory {arg} doesn't exist")
    def not_mandatory(arg, path):
        if path and not os.path.exists(path):
            raise Exception(f"Not existed {arg}: {path}")
    mandatory("args.path_to_log", args.path_to_log)
    mandatory("args.path_to_recording", args.path_to_recording)
    mandatory("args.path_to_samples", args.path_to_samples)
    not_mandatory("{args.path_to_recording_date=}", args.path_to_recording_date)

def main(args):
    _checks_args(args)
    start_date = GetRecordingStartDate(args.path_to_recording, args.path_to_recording_date)
    start_date = config.ConvertToLogZone(start_date)
    if not args.start_regex and not args.end_regex:
        regexes = config.GetRegexesForSampling()
        args.start_regex = regexes[0][0]
        args.end_regex = regexes[0][1]
        if len(regexes) > 1:
            logging.error("Number of regexes > 1 is not supported. Only the first one will be used")
    elif not (args.start_regex and args.end_regex):
        raise Exception("Inproper pair of start and end regex. Please provide both as arguments or in config")
    maxCount = -1
    if args.count:
        maxCount = args.count
    regexes = FindStartEndRegexes(args.path_to_log, args.start_regex, args.end_regex, args.from_line, maxCount)
    if args.path_to_search_lines:
        with open(args.lines_save_to, "w") as f:
            array = []
            for start_end in regexes:
                array.append(start_end[0].line_number)
                array.append(start_end[1].line_number)
            f.write("\n".join(array))
    sample_pathes = ExtractSamples(start_date, regexes, args.path_to_recording, args.path_to_samples)
    logging.info(f"Created: {sample_pathes}")
