#!/bin/bash
set -e

# Wait for database to be ready (only needed if using Docker Compose)
# while ! nc -z $DB_HOST $DB_PORT; do
#   echo "Waiting for database..."
#   sleep 2
# done

# Apply migrations
python manage.py migrate

# Create superuser if enabled
if [ "$CREATE_SUPERUSER" = "true" ]; then
    python manage.py createsuperuser --noinput || true
fi

# Collect static files
python manage.py collectstatic --noinput

exec "$@"