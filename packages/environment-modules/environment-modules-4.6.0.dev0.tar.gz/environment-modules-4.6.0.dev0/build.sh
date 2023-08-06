#!/bin/bash
set -euo pipefail
build_dir="$(readlink -m $1)"
install_tmp="$(readlink -m $2)"
prefix="$(readlink -m $3)"
TOP="$PWD"

configure_options="--prefix=$prefix"

# let's speed things up a bit; tell make to use some parallelism
NCPU=$(getconf _NPROCESSORS_CONF)
j=$((NCPU < 10 ? NCPU * 3 : 30))
export MAKE="make -j $j"

untar() {
    set +x
    package="$1"
    tar="$TOP/vendor/$package.tar.bz2"
    dst="$build_dir/$package"

    set -x
    mkdir -p $dst
    tar -xf "$tar" -C "$dst" --strip-components 1

    echo "$dst"
}

build() {
    set +x
    package="$1"
    tar="$TOP/vendor/$package.tar.bz2"
    # XXX: I couldn't figure out a better way :(
    weird_path="$install_tmp$prefix"

    set -x
    cd "$(untar "$package")"
    ./configure $configure_options  # sic: splat the options
    make
    make install DESTDIR="$install_tmp"

    mv "$weird_path" "$install_tmp.tmp"
    rmdir -p "$(dirname "$weird_path")" || true
    mv "$install_tmp.tmp" "$install_tmp"
}

set -x

build environment-modules
