

set -ex



test -f ${PREFIX}/lib/libpng.a
test -f ${PREFIX}/lib/libpng.so
libpng-config --version
conda inspect linkages -p $PREFIX libpng
exit 0
