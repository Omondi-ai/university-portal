#!/bin/bash

set -e

# Wait for the database to be ready (only needed if using docker-compose)
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

exec "$@"