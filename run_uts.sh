#!/bin/bash
./make_frb.sh && /tmp/frb/build/uts/tests && ./make_dlt.sh && ./python.sh -m pytest $(find -name "ut_*.py")
