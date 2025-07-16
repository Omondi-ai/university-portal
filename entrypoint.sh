#!/bin/bash
set -e

# Run migrations
python manage.py migrate

# Create superuser (only first deploy)
if [ "$CREATE_SUPERUSER" = "true" ]; then
    python manage.py createsuperuser --noinput || true
fi

# Start server
exec "$@"