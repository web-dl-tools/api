#!/bin/sh

until pg_isready -h postgres -p 5432 -d $POSTGRES_DB -U $POSTGRES_USER; do
    echo 'Waiting until PostgreSQL server is ready...'
    sleep 1
done
echo 'PostgreSQL server is up and ready. Continuing...'

exec "$@"
