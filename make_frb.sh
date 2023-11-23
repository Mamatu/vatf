#!/bin/bash
set -e

build () {
  VATF_PWD=$PWD
  FRB_PROJECT=$VATF_PWD/bin
  rm -r $FRB_PROJECT/build | true
  mkdir -p $FRB_PROJECT/build
  cd $FRB_PROJECT/build
  cmake -DCMAKE_INSTALL_PREFIX:PATH=$VATF_PWD/bin $VATF_PWD/file_ring_buffer
  make -j4
  make install
  cd -
}

build
