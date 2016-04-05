#!/bin/bash

# We should check if 8000 port is free and kill it

NAME="geo-geschenk"
HOST="127.0.0.1:8000"
FLASKDIR=/home/ing/PycharmProjects/geo-geschenk-server/geo-geschenk-server/app
VENVDIR=/home/ing/PycharmProjects/geo-geschenk-server/virtualenv
GUNICORN=/home/ing/PycharmProjects/geo-geschenk-server/virtualenv/bin/gunicorn
USER=$USER
NUM_WORKERS=1
FLASK_WSGI_MODULE=wsgi

echo "Starting $NAME"

# activate the virtualenv
cd $VENVDIR
source bin/activate

export PYTHONPATH=$FLASKDIR:$PYTHONPATH

# Start your unicorn
exec ${GUNICORN} ${FLASK_WSGI_MODULE}:app -b ${HOST} \
  --name $NAME \
  --worker-class eventlet \
  --workers $NUM_WORKERS \
  --user=$USER \
  --enable-stdio-inheritance \
  --access-logfile /home/ing/PycharmProjects/geo-geschenk-server/geo-geschenk-server/logs/gunicorn-access.log \
  --error-logfile /home/ing/PycharmProjects/geo-geschenk-server/geo-geschenk-server/logs/gunicorn-error.log \
  -R \
  --reload