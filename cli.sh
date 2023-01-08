#!/usr/bin/env sh

export PYTHONPATH="${PYTHONPATH}:src/"
python ./src/cli.py "$@"
