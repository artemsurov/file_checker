#!/bin/sh
python manage.py migrate
gunicorn -w 3 conf.wsgi:application --bind 0.0.0.0:9000 --reload
