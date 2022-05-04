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

find ${ROOT_DIR} -name "*.ogg" | parallel -I % --max-args 1 --jobs $JOBS PYTHONPATH=. python3 tools/python3/ogg_to_mfcc.py % %.png
