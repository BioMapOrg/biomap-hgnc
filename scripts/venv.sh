#!/usr/bin/bash

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

VENVPATH=$SCRIPTDIR/../.venv 
PACKAGE_NAME_MATCHER="name='\(.*\)',"
PACKAGE=$(expr match $(grep name $SCRIPTDIR/../setup.py) $PACKAGE_NAME_MATCHER)
VENV=$VENVPATH/$PACKAGE 

if [ ! -d $VENV ]; then
    python3 -m venv $VENV 
    source $VENV/bin/activate
	pip install --upgrade pip
    pip install -r $VENVPATH/requirements.txt
else
    source $VENV/bin/activate 
fi
