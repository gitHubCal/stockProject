#!/bin/bash

cd test
ln -s ${GXX} g++
cp ../xcrun .
cp ../xcodebuild .
export PATH=${PWD}:${PATH}
qmake hello.pro
make
./hello


set -ex



test -f $PREFIX/lib/libQt5WebEngine.so
test -f $PREFIX/plugins/sqldrivers/libqsqlite${SHLIB_EXT}
exit 0
