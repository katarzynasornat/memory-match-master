#!/bin/bash
set -e

if [ -n "$POSTGRES_HOST" ]; then
  echo "Waiting for PostgreSQL to be ready at $POSTGRES_HOST..."
  # Wait for PostgreSQL port to be open
  while ! nc -z "$POSTGRES_HOST" 5432; do
    >&2 echo "PostgreSQL is unavailable - sleeping"
    sleep 1
  done
else
  echo "POSTGRES_HOST not set, skipping netcat check (assuming managed DB or different config)"
fi

# Give PostgreSQL a moment to fully initialize
sleep 2

echo "PostgreSQL is up - running migrations"
cd /app/backend
uv run alembic upgrade head

echo "Starting supervisor to manage nginx and FastAPI"
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
