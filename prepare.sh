#!/bin/sh

echo 'Migrating...'
python manage.py migrate
echo 'Migration complete.'
