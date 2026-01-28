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
uv run alembic upgrade head

echo "Starting FastAPI server"
exec uv run uvicorn app.main:app --host 0.0.0.0 --port 3000
