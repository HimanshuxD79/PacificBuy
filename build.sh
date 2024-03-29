#!/usr/bin/env bash
# exit on error
set -o errexit
pip install django 
pip install gunicorn
pip install whitenoise
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate
