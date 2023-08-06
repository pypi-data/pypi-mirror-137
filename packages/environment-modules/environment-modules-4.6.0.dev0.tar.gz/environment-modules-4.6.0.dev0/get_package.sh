#!/bin/bash
# we vendor the tarballs directly because pip's tarball handling clobbers mtimes
# which can make make(1) make the wrong decisions (e.g. configure.ac is newer than aclocal.m4)
set -eu
package="$1"
url="$2"
tar=vendor/$package.tar.bz2

set -x
if [ -f $tar ]; then
    echo $package already downloaded
else
    mkdir -p "$(dirname $tar)"
    wget --no-check-certificate $url -O $tar
fi
