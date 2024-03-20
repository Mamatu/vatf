#!/bin/bash

LOG_CLI_LEVEL=INFO

if [[ ! -z $LOG_CLI_LEVEL ]]; then
    export LOG_CLI_LEVEL=$1
fi

./build_commands.sh Debug && LD_PRELOAD=$FBR_LD_PRELOAD bin/frb_tests && ./build_dlt.sh && ./python.sh -m pytest --log-cli-level=$LOG_CLI_LEVEL $(find -name "ut_*.py" -not -path "./utils/pylibcommons/*")
#./build_commands.sh && bin/frb_tests Debug && ./build_dlt.sh && ./python.sh -m pytest --log-cli-level=DEBUG $(find -name "ut_*.py" -not -path "./utils/pylibcommons/*")
