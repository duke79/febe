#!/usr/bin/env bash

#!/bin/bash

#source /code/lib/batch/paths.sh
#export PYTHONPATH="$ROOT_PATH":"${PYTHONPATH}"
#echo $PYTHONPATH
#python "$LIB_PATH/py/flask_app/runserver.py"
#pipenv run gunicorn run:app -b 192.168.1.102:5000 -w $(( 2 * `cat /proc/cpuinfo | grep 'core id' | wc -l` + 1 ))
#which python
#ln -s /usr/bin/python3 /usr/bin/python --force

#sudo python -m pip install -r /code/lib/py/requirements.txt

sudo ln -s /usr/bin/python3 /usr/bin/python --force
sudo ln -s /usr/bin/pip3 /usr/bin/pip --force
#cat /usr/local/lib/python3.6/dist-packages/gunicorn/util.py
python --version
#export PYTHONUNBUFFERED=TRUE

export FLASK_APP_MODULE="lib.py.flask_app.app:app"

gunicorn $FLASK_APP_MODULE \
    -b 0.0.0.0:5555 \
    --preload --log-level debug &
#    --spew

#export GUNICORN_FD="3"

gunicorn $FLASK_APP_MODULE \
    --bind 0.0.0.0:5565 \
    --certfile="/code/lib/py/flask_app/app/ssh/host.cert" \
    --keyfile="/code/lib/py/flask_app/app/ssh/host.key" \
    --preload --log-level debug
#    --spew

#gunicorn lib.py.flask_app.app:app --error-logfile=- --access-logfile=-