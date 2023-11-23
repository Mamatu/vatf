#!/bin/bash
set -e

MODE=Release
if [[ ! -z "$1" ]]; then
  MODE=$1
fi

build () {
  VATF_PWD=$PWD
  FRB_PROJECT=$VATF_PWD/bin
  rm -r $FRB_PROJECT/build | true
  mkdir -p $FRB_PROJECT/build
  cd $FRB_PROJECT/build
  cmake -DCMAKE_BUILD_TYPE=$MODE -DCMAKE_INSTALL_PREFIX:PATH=$VATF_PWD/bin $VATF_PWD/file_ring_buffer
  make -j4
  make install
  cd -
}

build
