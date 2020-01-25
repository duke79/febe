#!/usr/bin/env bash

BATCH_PATH="`dirname \"$0\"`"              # relative
BATCH_PATH="`( cd \"$BATCH_PATH\" && pwd )`"  # absolutized and normalized

PYTHONPATH="`( cd \"$BATCH_PATH/../..\" && pwd )`"  # absolutized and normalized

export PYTHONPATH=$PYTHONPATH
python3 -m src.flask_app.scripts.runserver.py
