#!/bin/bash
set -e

FRB_PROJECT=/tmp/frb

build () {
  VATF_PWD=$PWD
  rm -r $FRB_PROJECT/build | true
  mkdir -p $FRB_PROJECT/build
  cd $FRB_PROJECT/build
  cmake $VATF_PWD/file_ring_buffer
  make
  cd -
}

build
