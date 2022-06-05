#!/bin/bash
./python.sh -m unittest \
  api/tests/mkdir.py \
  api/tests/player.py \
  api/tests/wait.py \
  utils/tests/os_proxy.py \
  utils/tests/config_loader.py \
  utils/tests/gstreamer.py \
  utils/tests/rosa.py \
  utils/tests/utils.py \
  utils/tests/thread.py \
  api/tests/log_snapshot.py \
  api/tests/sampling.py
