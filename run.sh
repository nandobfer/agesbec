#!/bin/bash

if [[ $# == 0 ]]
then
    cd /home/suporte/siscomex

    screen -X -S siscomex kill
    screen -X -S credenciamento kill
    screen -X -S api kill

    screen -m -d -S siscomex python3 controle_acesso.py
    screen -m -d -S credenciamento python3 credenciamento_pessoas.py
    cd ../api
    screen -m -d -S api yarn start
fi

if [[ $1 ]]
then
    if [[ $1 == '-u' ]]
    then
        cd /home/suporte/siscomex

        screen -X -S siscomex kill
        screen -X -S credenciamento kill
        screen -X -S api kill
        git stash -u
        git pull
        chmod +x run.sh
        screen -m -d -S siscomex python3 controle_acesso.py
        screen -m -d -S credenciamento python3 credenciamento_pessoas.py
        cd ../api
        screen -m -d -S api yarn start
    fi
fi
