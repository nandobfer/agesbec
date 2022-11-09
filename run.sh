#!/bin/bash

if [[ $# == 0 ]]
then
    python3 app.py
fi

if [[ $1 ]]
then
    if [[ $1 == '-u' ]]
    then
        git stash -u && git pull && chmod +x run.sh && python3 app.py
    fi
fi
