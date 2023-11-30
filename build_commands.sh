#!/bin/bash

MODE=Release
if [[ ! -z "$1" ]]; then
  MODE=$1
fi

./build_frb.sh $MODE
