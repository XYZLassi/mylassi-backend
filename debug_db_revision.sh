#!/usr/bin/env sh

export PYTHONPATH="${PYTHONPATH}:src/"
alembic revision --autogenerate