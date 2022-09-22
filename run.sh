#!/bin/bash
git stash -u && git pull && chmod +x run.sh && python3 controle_acesso.py