#!/bin/bash

bash configure --prefix=$PREFIX

make -j${CPU_COUNT} ${VERBOSE_AT}
make check
make install
