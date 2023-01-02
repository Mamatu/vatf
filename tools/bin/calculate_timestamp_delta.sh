#!/bin/bash
#
#   bash tools/calculate_timestamp_delta.sh "2022/02/03 13:53:36.773388" "%Y/%m/%d %H:%M:%S.%f" "2022-02-03 13:53:29.659565" "%Y-%m-%d %H:%M:%S.%f"
#

PYTHONPATH=. python3 tools/calculate_timestamp_delta.py "$@"
