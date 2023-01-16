#!/bin/bash
./make_dlt.sh && ./python.sh -m pytest $(find -name "ut_*.py")
