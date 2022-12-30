#!/bin/bash
ut_path=$1
./make_dlt.sh && ./python.sh -m pytest -s $ut_path
