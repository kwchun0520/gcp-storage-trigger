!usr/bin/env bash
set -x
export $(cat .env | xargs)
poetry run python main.py