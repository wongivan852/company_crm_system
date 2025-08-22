#!/bin/bash

# CRM Startup Script - Port 8083
# Complete system with 1010 customers

echo "================================================"
echo "    CRM SYSTEM - PORT 8083"
echo "    1010 Customers Ready for Access"
echo "================================================"

cd /home/user/krystal-company-apps/company_crm_system/crm_project
source ../.venv/bin/activate

# Stop any existing servers
pkill -f "runserver.*8083" 2>/dev/null || true
sleep 1

echo "🚀 Starting CRM server on port 8083..."
echo ""
echo "🌐 Localhost Access:"
echo "   http://localhost:8083/admin/"
echo ""
echo "👤 Login Credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "🌍 Internet Access (after firewall config):"
echo "   http://203.186.246.162:8083/"
echo ""
echo "🔥 To enable internet access, run:"
echo "   sudo ufw allow 8083/tcp"
echo ""
echo "Press Ctrl+C to stop server"
echo "================================================"

# Start server
python manage.py runserver 0.0.0.0:8083 --settings=sqlite_settings --noreload
