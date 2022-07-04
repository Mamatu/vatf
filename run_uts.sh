#!/bin/bash
./make_dlt.sh && \
./python.sh -m unittest \
  api/uts/ut_mkdir.py \
  api/uts/ut_player.py \
  api/uts/ut_wait.py \
  utils/uts/ut_os_proxy.py \
  utils/uts/ut_gstreamer.py \
  utils/uts/ut_rosa.py \
  utils/uts/ut_utils.py \
  utils/uts/ut_thread.py \
  api/uts/ut_log_snapshot.py && \
./python.sh -m pytest api/uts/ut_sampling.py api/uts/ut_log_snapshot.py utils/uts/ut_config.py
