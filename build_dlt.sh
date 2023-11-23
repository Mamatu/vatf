#!/bin/bash
set -e

MODE=Release
if [[ ! -z "$1" ]]; then
  MODE=$1
fi

DLT_PROJECT=/tmp/dlt-project

make_and_install () {
  git clone --branch v2.18.10 https://github.com/COVESA/dlt-daemon.git $DLT_PROJECT/dlt-daemon
  mkdir -p $DLT_PROJECT/dlt-daemon/build
  cd $DLT_PROJECT/dlt-daemon/build
  cmake .. -DCMAKE_BUILD_TYPE=$MODE -DCMAKE_INSTALL_PREFIX=$DLT_PROJECT/rootfs/ -DBUILD_SHARED_LIBS=OFF
  make -j4
  make install
  cd -
}

if [ ! -d "$DLT_PROJECT" ]
then
  make_and_install
fi
