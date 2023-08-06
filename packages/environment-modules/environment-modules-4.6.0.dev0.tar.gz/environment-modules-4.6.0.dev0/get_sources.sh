#!/bin/bash
set -eu

source versions.sh

./get_package.sh environment-modules https://github.com/cea-hpc/modules/releases/download/v$version/modules-$version.tar.bz2
