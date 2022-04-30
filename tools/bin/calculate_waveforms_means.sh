#!/bin/bash

JOBS=4
ROOT_DIR=""
PYARGS=""

while getopts j:r: flag
do
    case "${flag}" in
        j) JOBS=${OPTARG};;
        r) ROOT_DIR=${OPTARG};;
        pyargs) PYARGS=${OPTARG};;
    esac
done

find ${ROOT_DIR} -name "*.ogg" -o -name "*.wav" | parallel -I % --max-args 1 --jobs $JOBS python3 tools/python3/calculate_waveform_means.py % %.means.npz $PYARGS
