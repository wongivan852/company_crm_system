#!/bin/bash

# CRM Internet Access Startup Script
# Makes CRM accessible from internet on port 8082

echo "========================================================="
echo "    CRM SYSTEM - INTERNET ACCESS CONFIGURATION"
echo "    1010 Customers | Port 8082 | Internet Accessible"
echo "========================================================="

cd /home/user/krystal-company-apps/company_crm_system/crm_project
source ../.venv/bin/activate

# Display network information
echo "🌐 Network Configuration:"
echo "   • Server will bind to: 0.0.0.0:8082 (all interfaces)"
echo "   • Accessible from: Internet + Intranet"
echo "   • Local access: http://localhost:8082/"
echo ""

# Get external IP for reference
EXTERNAL_IP=$(curl -s ifconfig.me 2>/dev/null || echo "Unable to detect external IP")
if [ "$EXTERNAL_IP" != "Unable to detect external IP" ]; then
    echo "🌍 External access (if firewall allows):"
    echo "   • http://$EXTERNAL_IP:8082/"
    echo "   • Admin: http://$EXTERNAL_IP:8082/admin/"
    echo ""
fi

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
echo "🚀 Starting CRM server with internet access..."
echo "🔑 Admin login: admin / admin123"
echo ""
echo "⚠️  SECURITY NOTE: This is development mode"
echo "   For production, use HTTPS and proper security"
echo ""
echo "Press Ctrl+C to stop server"
echo "========================================================="

# Start server on all interfaces (0.0.0.0) for internet access
python manage.py runserver 0.0.0.0:8082 --settings=sqlite_settings
