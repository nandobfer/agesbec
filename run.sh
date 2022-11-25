#!/bin/bash

if [[ $# == 0 ]]
then
    screen -m -d -S siscomex python3 app.py
fi

if [[ $1 ]]
then
    if [[ $1 == '-u' ]]
    then
        screen -X -S siscomex kill
        git stash -u
        git pull
        chmod +x run.sh
        screen -m -d -S siscomex python3 app.py
    fi
fi
