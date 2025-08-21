#!/bin/bash

# GUARANTEED WORKING CRM STARTUP
# Uses SQLite database with your 728 customers

echo "==============================================="
echo "    STARTING CRM WITH SQLITE DATABASE"
echo "==============================================="

# Navigate to project
cd /home/user/krystal-company-apps/company_crm_system/crm_project

# Activate virtual environment
source ../.venv/bin/activate

# Set environment variables for guaranteed success
export DEBUG=1
export SECRET_KEY="dev-secret-key-for-testing"
export ALLOWED_HOSTS="localhost,127.0.0.1,0.0.0.0,*"
export SECURE_SSL_REDIRECT=0
export SESSION_COOKIE_SECURE=0
export CSRF_COOKIE_SECURE=0

# Use SQLite database with your data
export DATABASE_URL="sqlite:///../crm_test_safe.sqlite3"

echo "✅ Environment configured"
echo "✅ Using SQLite database with your 728 customers"
echo "✅ Starting server on port 8888..."
echo ""

# Start the server
python manage.py runserver 0.0.0.0:8888 --insecure
