#!/usr/bin/env bash

chown www-data:www-data /var/log

python manage.py compilemessages
python manage.py collectstatic --no-input
python manage.py migrate
uwsgi --strict --ini /opt/app/uwsgi.ini
