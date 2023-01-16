__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

import argparse
import sys
import logging

parser = argparse.ArgumentParser(description='vatf.api - to execute test')
subparsers = parser.add_subparsers(help='sub-command help')
parser_play = subparsers.add_parser('play', help='play help')
parser_play.add_argument('--path', type=str, help='Path to audio file')

parser_sleep = subparsers.add_parser('sleep', help='sleep help')
parser_sleep.add_argument('--regex', type=str, help='Sleep until regex will be available in logs')
parser_sleep.add_argument('--path_to_log', type=str, help='log with regexes')
parser_sleep.add_argument('--timeout', type=float, help='timeout of sleep')
parser_sleep.add_argument('--delta', type=float, help='in the case of regex, it is value of sleep duration beetwen examination of regex')

parser_mkdir = subparsers.add_parser('mkdir', help='mkdir help')
parser_mkdir.add_argument('--path_to_counter', type=str, help="makes folder in path with incremented suffix")
parser_mkdir.add_argument('--output_save_to', type=str, help="save output of operation to file")

parser_sampling = subparsers.add_parser('sampling', help='sampling help')
parser_sampling.add_argument('--path_to_log', type=str, help="path to log with informations about sampling")
parser_sampling.add_argument('--path_to_recording', type=str, help="path to recording from where samples can be extracted")
parser_sampling.add_argument('--path_to_recording_date', type=str, help="(optional) path to file which contains recording creation date. If it is not specified, it will take date from recording file")
parser_sampling.add_argument('--path_to_recording_info', type=str, help="path to json file which includes recording path, recording creation time, audio format (optional)")
parser_sampling.add_argument('--path_to_samples', type=str, help="path to log with informations about sampling")
parser_sampling.add_argument('--start_regex', type=str, help="regex of sample begin")
parser_sampling.add_argument('--end_regex', type=str, help="regex of sample end")
parser_sampling.add_argument('--from_line', type=int, help="start search from line")
parser_sampling.add_argument('--count', type=int, help="stop after count of specific occurances")
parser_sampling.add_argument('--path_to_search_lines', type=str, help="path to file where is stored line in log where regex was found. If count is higher than 1, then it will contains set of lines")
parser_sampling.add_argument('--path_to_search_start_date', action="store_true", help="path to file where is date from search is started")

parser_logger = subparsers.add_parser('logger', help='logger utils')
parser_logger.add_argument('--path_to_input_log', type=str, help="path to file of full log")
parser_logger.add_argument('--path_to_output_dir', type=str, help="path to output directory")
parser_logger.add_argument('--output_file_name', type=str, help="output file name as default 'session.log'")

parser_config = subparsers.add_parser('config', help='read config for test')
parser_config.add_argument('--path_to_config', type=str, help='path to config')

args = parser.parse_args()

if __name__ == "__main__":
    from vatf_utils import config
    import importlib
    logging.basicConfig(level=logging.INFO)
    subprogram = sys.argv[1]
    module = importlib.import_module(subprogram)
    module.main(args)
