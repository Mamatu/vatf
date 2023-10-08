#!/bin/bash
set -e

FRB_PROJECT=/tmp/frb

build () {
  VATF_PWD=$PWD
  mkdir -p $FRB_PROJECT/build
  cd $FRB_PROJECT/build
  cmake $VATF_PWD/file_ring_buffer
  make
  cd -
}

if [ ! -d "$FRB_PROJECT" ]
then
  build
fi
