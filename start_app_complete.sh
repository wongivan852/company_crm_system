#!/bin/bash

# Complete App Startup Script for CRM System
# This will handle all setup and start the application

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[$(date +'%H:%M:%S')] WARNING:${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%H:%M:%S')] ERROR:${NC} $1"
    exit 1
}

info() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')] INFO:${NC} $1"
}

# Change to project root
cd "$(dirname "$0")"

log "Starting CRM System Setup and Launch"

# Check if virtual environment exists
if [[ ! -d ".venv" ]]; then
    log "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
log "Activating virtual environment..."
source .venv/bin/activate

# Install/upgrade dependencies
log "Installing dependencies..."
pip install -r requirements.txt

# Change to Django project directory
cd crm_project

# Create missing directories
log "Creating required directories..."
mkdir -p static
mkdir -p staticfiles
mkdir -p media
mkdir -p logs
mkdir -p templates/static

# Set proper permissions
chmod 755 static staticfiles media logs

# Check database connectivity
log "Checking database connectivity..."
python manage.py check --database default

# Run migrations
log "Running database migrations..."
python manage.py migrate

# Collect static files
log "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if none exists
log "Checking for superuser..."
SUPERUSER_EXISTS=$(python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
print('yes' if User.objects.filter(is_superuser=True).exists() else 'no')
")

if [[ "$SUPERUSER_EXISTS" == "no" ]]; then
    warn "No superuser found. Creating default admin user..."
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Created superuser: admin/admin123')
else:
    print('Admin user already exists')
"
    warn "Default superuser created: admin/admin123"
    warn "Please change this password in production!"
fi

# Verify data integrity
log "Verifying data integrity..."
CUSTOMER_COUNT=$(python manage.py shell -c "
from crm.models import Customer
print(Customer.objects.count())
")

YOUTUBE_COUNT=$(python manage.py shell -c "
from crm.models import Customer
print(Customer.objects.filter(customer_type='youtuber').count())
")

REGULAR_COUNT=$((CUSTOMER_COUNT - YOUTUBE_COUNT))

info "Database Summary:"
info "  - Total Customers: $CUSTOMER_COUNT"
info "  - Regular Customers: $REGULAR_COUNT"  
info "  - YouTube Creators: $YOUTUBE_COUNT"

# Start the development server
log "Starting Django development server..."
info "The application will be available at:"
info "  - Main application: http://localhost:8000/"
info "  - Admin interface: http://localhost:8000/admin/"
info "  - API endpoints: http://localhost:8000/api/"

if [[ "$SUPERUSER_EXISTS" == "no" ]]; then
    info "  - Admin login: admin / admin123"
fi

info ""
info "Press Ctrl+C to stop the server"
info "========================================"

# Start the server
python manage.py runserver 0.0.0.0:8000
