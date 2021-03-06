#!/bin/bash

JOBS=4
ROOT_DIR=""

while getopts j:r: flag
do
    case "${flag}" in
        j) JOBS=${OPTARG};;
        r) ROOT_DIR=${OPTARG};;
    esac
done

find ${ROOT_DIR} -name "*.pcm" | parallel -I % --max-args 1 --jobs $JOBS PYTHONPATH=. python3 vatf/utils/papy.py --convert --input % --output %.wav --tool ffmpeg --audio_config s16le,1,44100
