#!/bin/bash

# CRM System Launcher with Monitoring
# Starts the application and provides access information

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Functions
log() { echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $1"; }
info() { echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"; }
warn() { echo -e "${YELLOW}[$(date +'%H:%M:%S')]${NC} $1"; }

# Change to project directory
cd "$(dirname "$0")"

# Header
clear
echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    CRM SYSTEM LAUNCHER                      ║${NC}"
echo -e "${BLUE}║                  Integrated Solution                        ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo

# Activate virtual environment
log "Activating virtual environment..."
source .venv/bin/activate

# Change to Django project
cd crm_project

# Quick system check
log "Performing system check..."
python manage.py check --database default

# Get database stats
log "Loading database statistics..."
STATS=$(python manage.py shell -c "
from crm.models import Customer
total = Customer.objects.count()
youtube = Customer.objects.filter(customer_type='youtuber').count()
regular = total - youtube
corporate = Customer.objects.filter(customer_type='corporate').count()
student = Customer.objects.filter(customer_type='student').count()
individual = Customer.objects.filter(customer_type='individual').count()
print(f'{total},{youtube},{regular},{corporate},{student},{individual}')
")

IFS=',' read -r TOTAL YOUTUBE REGULAR CORPORATE STUDENT INDIVIDUAL <<< "$STATS"

# Display system status
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}                      SYSTEM STATUS                            ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}📊 Database Summary:${NC}"
echo "   • Total Customers: $TOTAL"
echo "   • YouTube Creators: $YOUTUBE"
echo "   • Regular Customers: $REGULAR"
echo "     ├─ Individual: $INDIVIDUAL"
echo "     ├─ Corporate: $CORPORATE"
echo "     └─ Student: $STUDENT"
echo

echo -e "${GREEN}🌐 Access Information:${NC}"
echo "   • Main Application: http://localhost:8000/"
echo "   • Admin Interface:  http://localhost:8000/admin/"
echo "   • API Endpoints:    http://localhost:8000/api/"
echo

echo -e "${GREEN}👤 Admin Access:${NC}"
echo "   • Username: admin"
echo "   • Password: admin123"
echo "   • Note: Change password in production!"
echo

echo -e "${GREEN}🔧 Available Features:${NC}"
echo "   • Customer Management (All Types)"
echo "   • YouTube Creator Integration"
echo "   • Course & Conference Management"
echo "   • Communication Logging"
echo "   • REST API Access"
echo "   • Admin Dashboard"
echo

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}🚀 Starting Django Development Server...${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo

# Start server with custom settings
export DJANGO_SETTINGS_MODULE=crm_project.settings
python manage.py runserver 0.0.0.0:8000
