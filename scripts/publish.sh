#!/usr/bin/bash

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

source $SCRIPTDIR/venv.sh

$SCRIPTDIR/clean.sh
pip install --upgrade setuptools wheel
python setup.py sdist bdist_wheel
twine upload dist/*
$SCRIPTDIR/clean.sh
