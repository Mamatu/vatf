#!/bin/bash
./init.sh && bin/frb_tests && ./make_dlt.sh && ./python.sh -m pytest $(find -name "ut_*.py" -not -path "./utils/pylibcommons/*")
