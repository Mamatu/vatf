#!/bin/bash
./make_dlt.sh && \
./python.sh -m unittest \
  executor/uts/ut_mkdir.py \
  executor/uts/ut_player.py \
  executor/uts/ut_wait.py \
  utils/uts/ut_os_proxy.py \
  utils/uts/ut_gstreamer.py \
  utils/uts/ut_rosa.py \
  utils/uts/ut_utils.py \
  utils/uts/ut_thread.py \
  generator/uts/ut_gen_tests.py \
  generator/uts/ut_player.py \
  generator/uts/ut_wait.py && \
./python.sh -m pytest executor/uts/ut_shell.py executor/uts/ut_sampling.py utils/uts/ut_config.py executor/uts/ut_search.py executor/uts/ut_log_snapshot_dlt.py executor/uts/ut_wait_dlt.py utils/uts/ut_utils_func_info.py utils/uts/ut_wait_conditioner.py
