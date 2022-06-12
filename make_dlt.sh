#!/bin/bash

DLT_PROJECT=/tmp/dlt-project

make_and_install () {
  mkdir /tmp/dlt/bin
  git clone -b v2.17.0 https://github.com/COVESA/dlt-daemon.git $DLT_PROJECT/dlt-daemon
  mkdir -p $DLT_PROJECT/dlt-daemon/build
  cd $DLT_PROJECT/dlt-daemon/build
  cmake .. -DCMAKE_INSTALL_PREFIX=$DLT_PROJECT/rootfs/
  make -j4
  make install
  cd -
}

if [ ! -d "$DLT_PROJECT" ]
then
  make_and_install
fi
