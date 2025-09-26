#!/bin/bash
set -e

echo "🚀 Starting KCH FastAPI application..."

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
POSTGRES_HOST=${POSTGRES_HOST:-postgres}
POSTGRES_PORT=${POSTGRES_PORT:-5432}
while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 2
done

echo "✅ PostgreSQL is ready!"

# Initialize database tables
echo "🔧 Initializing database tables..."
python init_database.py || echo "⚠️  Database initialization failed or already exists"

# Start the FastAPI application
echo "🎯 Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
