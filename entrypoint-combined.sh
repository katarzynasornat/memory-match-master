#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
# Wait for PostgreSQL port to be open
while ! nc -z "$POSTGRES_HOST" 5432; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

# Give PostgreSQL a moment to fully initialize
sleep 2

echo "PostgreSQL is up - running migrations"
cd /app/backend
uv run alembic upgrade head

echo "Starting supervisor to manage nginx and FastAPI"
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
