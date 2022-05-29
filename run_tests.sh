#!/bin/bash
./python.sh -m unittest \
  generator/tests/gen_tests.py \
  generator/tests/player.py \
  generator/tests/wait.py \
  executor/tests/mkdir.py \
  executor/tests/player.py \
  executor/tests/wait.py \
  utils/tests/os_proxy.py \
  utils/tests/config_loader.py \
  utils/tests/gstreamer.py \
  utils/tests/rosa.py \
  utils/tests/utils.py \
  utils/tests/thread.py \
  executor/tests/log_snapshot.py \
  executor/tests/sampling.py \
  api/tests/test.py
