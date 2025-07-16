#!/bin/bash
set -e

# Apply migrations
python manage.py migrate

# Create superuser if enabled
if [ "$CREATE_SUPERUSER" = "true" ]; then
    python manage.py createsuperuser --noinput || true
fi

# Collect static files
python manage.py collectstatic --noinput

exec "$@"