#!/usr/bin/bash

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
ROOT=$SCRIPTDIR/..

rm -rf $ROOT/biomap_hgnc.egg-info
rm -rf $ROOT/build
rm -rf $ROOT/dist
