#!/bin/sh

python manage.py migrate

exec "$@"
