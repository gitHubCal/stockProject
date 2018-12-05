#!/bin/bash

set -e

genrb de.txt
echo "de.res" > list.txt
pkgdata -p mybundle list.txt


set -ex



test -f $PREFIX/lib/libicudata.a
test -f $PREFIX/lib/libicudata.so.58.2
test -f $PREFIX/lib/libicui18n.a
test -f $PREFIX/lib/libicui18n.so.58.2
test -f $PREFIX/lib/libicuio.a
test -f $PREFIX/lib/libicuio.so.58.2
test -f $PREFIX/lib/libicutest.a
test -f $PREFIX/lib/libicutest.so.58.2
test -f $PREFIX/lib/libicutu.a
test -f $PREFIX/lib/libicutu.so.58.2
test -f $PREFIX/lib/libicuuc.a
test -f $PREFIX/lib/libicuuc.so.58.2
genbrk --help
gencfu --help
gencnval --help
gendict --help
icuinfo --help
icu-config --help
makeconv gb-18030-2000.ucm
conda inspect linkages -p $PREFIX icu
exit 0
