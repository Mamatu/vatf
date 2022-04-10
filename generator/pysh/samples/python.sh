#!/bin/sh
set -e
set -o xtrace
PYTHONPATH=../.. python $@
