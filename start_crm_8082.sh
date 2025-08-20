#!/bin/bash

# CRM Startup Script - Port 8082
# Complete integrated system with 1010 customers

echo "=================================================="
echo "    CRM SYSTEM - COMPLETE INTEGRATION"
echo "    1010 Customers (961 Regular + 49 YouTube)"
echo "=================================================="

cd /home/user/krystal-company-apps/company_crm_system/crm_project
source ../.venv/bin/activate

# Verify database
echo "📊 Verifying database..."
python manage.py shell --settings=sqlite_settings -c "
from crm.models import Customer
total = Customer.objects.count()
youtube = Customer.objects.filter(customer_type='youtuber').count()
regular = total - youtube
print(f'✅ Database ready: {total} customers')
print(f'   Regular: {regular}')
print(f'   YouTube: {youtube}')
"

echo ""
echo "🚀 Starting CRM server on port 8082..."
echo "🌐 Access: http://localhost:8082/"
echo "🔑 Admin: http://localhost:8082/admin/"
echo "👤 Login: admin / admin123"
echo ""
echo "Press Ctrl+C to stop server"
echo "=================================================="

# Start server
python manage.py runserver 0.0.0.0:8082 --settings=sqlite_settings
