#!/bin/bash
now=$(date +"%m_%d_%Y-%H%M%S")
zip -r results_$now.zip $(find -maxdepth 1 -type d | xargs -I % find % -name "session_*")
