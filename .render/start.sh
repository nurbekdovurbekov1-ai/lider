#!/bin/bash
set -e

echo "🚀 Starting Lider Avto on Render..."

# Create necessary directories
mkdir -p media staticfiles

# Run migrations
echo "📦 Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Start gunicorn
echo "🚀 Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 90
