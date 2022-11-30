#!/bin/bash

if [[ $# == 0 ]]
then
    screen -m -d -S siscomex python3 controle_acesso.py
    screen -m -d -S credenciamento python3 credenciamento_pessoas.py
fi

if [[ $1 ]]
then
    if [[ $1 == '-u' ]]
    then
        screen -X -S siscomex kill
        screen -X -S credenciamento kill
        git stash -u
        git pull
        chmod +x run.sh
        screen -m -d -S siscomex python3 controle_acesso.py
        screen -m -d -S credenciamento python3 credenciamento_pessoas.py
    fi
fi
