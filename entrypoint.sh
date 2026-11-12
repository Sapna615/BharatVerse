#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Loading cultural data..."
python manage.py loaddata fixtures/initial_data.json || true

echo "Starting Gunicorn server..."
exec gunicorn bharatverse.wsgi:application --bind 0.0.0.0:8000
