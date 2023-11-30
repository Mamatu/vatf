#!/bin/bash
ut_path=$1
pytests_args=$2
./build_dlt.sh && ./python.sh -m pytest $pytests_args -s $ut_path
