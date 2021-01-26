#!/bin/bash
echo "Waiting for Daphne..."

while ! nc -z $WS_HOST $WS_PORT; do
  sleep 0.1
done

echo "Daphne started"

exec "$@"