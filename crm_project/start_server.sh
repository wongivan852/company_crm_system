#!/bin/bash

# CRM Server Startup Script
# Always runs on port 8000 for intranet access

echo "Starting CRM Server on port 8000..."
echo "Accessible via intranet at: http://[your-ip]:8000"
echo "Press Ctrl+C to stop the server"
echo "========================="

# Set environment variables if not already set
export DJANGO_SETTINGS_MODULE=crm_project.settings

# Run migrations if needed
echo "Checking for database migrations..."
python manage.py migrate --check || python manage.py migrate

# Collect static files for production-like serving
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Start the server on all interfaces, port 8000
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000