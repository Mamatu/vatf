#!/bin/bash
set -e
set -o xtrace

run_sample () {
  ./python.sh $1
  bash /tmp/$1.sh
  if [[ $? == 1 ]]
  then
    echo "exit 1"
    exit 1
  fi
}

scripts=($(ls | grep '.*\.py'))
for script in "${scripts[@]}"
do
  run_sample $script
done
