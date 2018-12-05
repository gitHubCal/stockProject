

set -ex



pcre-config --version
pcregrep --help
pcretest --help
test -f "${PREFIX}/include/pcre.h"
test -f "${PREFIX}/include/pcre_scanner.h"
test -f "${PREFIX}/include/pcre_stringpiece.h"
test -f "${PREFIX}/include/pcrecpp.h"
test -f "${PREFIX}/include/pcrecpparg.h"
test -f "${PREFIX}/include/pcreposix.h"
test -f "${PREFIX}/lib/libpcre.a"
test -f "${PREFIX}/lib/libpcre.so"
test -f "${PREFIX}/lib/libpcrecpp.a"
test -f "${PREFIX}/lib/libpcrecpp.so"
test -f "${PREFIX}/lib/libpcreposix.a"
test -f "${PREFIX}/lib/libpcreposix.so"
exit 0
