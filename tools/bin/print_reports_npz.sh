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

find ${ROOT_DIR} -name "*.npz" | parallel -I % --max-args 1 --jobs $JOBS PYTHONPATH=. python3 tools/python/print_reports_npz.py %
