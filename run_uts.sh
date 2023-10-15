#!/bin/bash
./init.sh && bin/uts/tests && ./make_dlt.sh && ./python.sh -m pytest $(find -name "ut_*.py" -not -path "./utils/pylibcommons/*")
