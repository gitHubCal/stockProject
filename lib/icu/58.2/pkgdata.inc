GENCCODE_ASSEMBLY_TYPE=-a gcc
SO=so
SOBJ=so
A=a
LIBPREFIX=lib
LIB_EXT_ORDER=.58.2
COMPILE=/home/calvin/python_projects/stockProject/bin/x86_64-conda_cos6-linux-gnu-cc -D_FORTIFY_SOURCE=2 -O2 -D_REENTRANT  -DU_HAVE_ELF_H=1 -DU_HAVE_ATOMIC=1 -DU_HAVE_STRTOD_L=1  -DU_ATTRIBUTE_DEPRECATED= -march=nocona -mtune=haswell -ftree-vectorize -fPIC -fstack-protector-strong -fno-plt -O2 -pipe -I/home/calvin/python_projects/stockProject/include -std=c99 -Wall -pedantic -Wshadow -Wpointer-arith -Wmissing-prototypes -Wwrite-strings   -c
LIBFLAGS=-I/home/calvin/python_projects/stockProject/include -DPIC -fPIC
GENLIB=/home/calvin/python_projects/stockProject/bin/x86_64-conda_cos6-linux-gnu-cc -march=nocona -mtune=haswell -ftree-vectorize -fPIC -fstack-protector-strong -fno-plt -O2 -pipe -I/home/calvin/python_projects/stockProject/include -std=c99 -Wall -pedantic -Wshadow -Wpointer-arith -Wmissing-prototypes -Wwrite-strings   -Wl,-O2 -Wl,--sort-common -Wl,--as-needed -Wl,-z,relro -Wl,-z,now -Wl,-rpath,/home/calvin/python_projects/stockProject/lib -L/home/calvin/python_projects/stockProject/lib  -shared -Wl,-Bsymbolic
LDICUDTFLAGS=-nodefaultlibs -nostdlib
LD_SONAME=-Wl,-soname -Wl,
RPATH_FLAGS=
BIR_LDFLAGS=-Wl,-Bsymbolic
AR=/home/calvin/python_projects/stockProject/bin/x86_64-conda_cos6-linux-gnu-ar
ARFLAGS=r
RANLIB=/home/calvin/python_projects/stockProject/bin/x86_64-conda_cos6-linux-gnu-ranlib
INSTALL_CMD=/usr/bin/install -c
