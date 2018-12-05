#!/bin/bash

# if [[ ${HOST} =~ .*darwin.* ]]; then
WITHOUT_X=--without-x
# fi

CPPFLAGS="${CPPFLAGS} -I${PREFIX}/include" \
LDFLAGS="${LDFLAGS} -L${PREFIX}/lib -Wl,-rpath,${PREFIX}/lib"  \
  ./configure --prefix=${PREFIX}   \
              --disable-systemd    \
              --disable-selinux    \
              --disable-xml-docs   \
              --with-launchd-agent-dir=${PREFIX}  \
              ${WITHOUT_X}
make -j${CPU_COUNT} ${VERBOSE_AT}
if [[ $(uname) != Darwin ]]; then
  make check
fi
make install
