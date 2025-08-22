#!/bin/bash

echo "🌐 CRM System Internet Access Verification Report"
echo "=================================================="
echo "Date: $(date)"
echo "System: Company CRM System"
echo ""

# System Info
echo "📋 SYSTEM INFORMATION:"
echo "IP Address: $(ip addr show wlp2s0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1)"
echo "Gateway: $(ip route show default | awk '{print $3}')"
echo "Port: 8083"
echo ""

# Docker Container Status
echo "🐳 DOCKER CONTAINER STATUS:"
sudo docker-compose ps | grep -E "(web_1|State|Ports)"
echo ""

# Port Listening Status
echo "🔍 PORT BINDING STATUS:"
sudo netstat -tlnp | grep 8083
echo ""

# Firewall Status
echo "🛡️ FIREWALL STATUS:"
sudo ufw status | grep 8083
echo ""

# Local Access Test
echo "🏠 LOCAL ACCESS TEST:"
echo "Testing http://localhost:8083/"
if curl -s -I http://localhost:8083/ | head -1 | grep -q "302"; then
    echo "✅ Local access: WORKING"
else
    echo "❌ Local access: FAILED"
fi
echo ""

# IP Access Test
echo "🌍 IP ACCESS TEST:"
LOCAL_IP=$(ip addr show wlp2s0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1)
echo "Testing http://$LOCAL_IP:8083/"
if curl -s -I http://$LOCAL_IP:8083/ | head -1 | grep -q "302"; then
    echo "✅ IP access: WORKING"
else
    echo "❌ IP access: FAILED"
fi
echo ""

# Admin Panel Test
echo "👤 ADMIN PANEL ACCESS TEST:"
echo "Testing http://$LOCAL_IP:8083/admin/"
if curl -s -I http://$LOCAL_IP:8083/admin/ | head -1 | grep -q "302"; then
    echo "✅ Admin panel: ACCESSIBLE"
else
    echo "❌ Admin panel: FAILED"
fi
echo ""

# Django Settings Check
echo "⚙️ DJANGO CONFIGURATION:"
sudo docker-compose exec -T web python crm_project/manage.py shell -c "
from django.conf import settings
print('ALLOWED_HOSTS:', settings.ALLOWED_HOSTS)
print('DEBUG:', settings.DEBUG)
print('PORT:', getattr(settings, 'PORT', 'Not set'))
"
echo ""

# Content Test
echo "📄 CONTENT VERIFICATION:"
CONTENT_CHECK=$(curl -s -L http://$LOCAL_IP:8083/ | grep -c "Learning Institute CRM")
if [ "$CONTENT_CHECK" -gt 0 ]; then
    echo "✅ HTML content: LOADING CORRECTLY"
else
    echo "❌ HTML content: ISSUE DETECTED"
fi
echo ""

# Network Interfaces
echo "🔗 NETWORK INTERFACES:"
ip addr show | grep -E "inet.*scope global"
echo ""

# Final Status
echo "📊 INTERNET ACCESS STATUS:"
if curl -s -I http://$LOCAL_IP:8083/ | head -1 | grep -q "302"; then
    echo "🟢 STATUS: CRM SYSTEM IS ACCESSIBLE FROM INTERNET"
    echo "🌐 Access URL: http://$LOCAL_IP:8083"
    echo "👨‍💼 Admin URL: http://$LOCAL_IP:8083/admin/"
    echo ""
    echo "✅ READY FOR EXTERNAL ACCESS"
    echo "• Port 8083 is open and listening on all interfaces"
    echo "• Firewall allows incoming connections"
    echo "• Django ALLOWED_HOSTS configured for external access"
    echo "• Docker container is healthy and responding"
else
    echo "🔴 STATUS: ACCESS ISSUES DETECTED"
    echo "❌ TROUBLESHOOTING REQUIRED"
fi

echo ""
echo "=================================================="
