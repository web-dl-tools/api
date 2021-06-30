#!/bin/sh

sleep $((60)) # Await for django to start.

while true; do
    python3 manage.py cleanup
    sleep $((24 * 60 * 60)) # 24 hours
done &
