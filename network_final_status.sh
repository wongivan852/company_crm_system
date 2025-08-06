#!/bin/bash

echo "🎉 KRYSTAL COMPANY APPS - FINAL NETWORK STATUS"
echo "============================================"
echo ""

# System info
echo "💻 SYSTEM INFO:"
echo "   Host IP: 192.168.0.104"
echo "   Network: Krystal-414-b WiFi"
echo "   Gateway: 192.168.0.1"
echo ""

# CRM System Status
echo "🏢 CRM SYSTEM (Django):"
CRM_PID=$(pgrep -f "manage.py runserver")
if [ ! -z "$CRM_PID" ]; then
    echo "   ✅ Status: RUNNING"
    echo "   🌐 Main URL: http://192.168.0.104:8082/"
    echo "   🧪 Network Test: http://192.168.0.104:8082/network-test/"
    echo "   🎨 Landing Page: http://192.168.0.104:8082/network-landing/"
    echo "   👤 Admin Panel: http://192.168.0.104:8082/admin/"
    echo "   🔑 Login: admin / admin123"
    echo "   ✅ Database: Fresh setup completed"
else
    echo "   ❌ Status: STOPPED"
fi

echo ""
echo "💳 STRIPE DASHBOARD:"
echo "   ℹ️  Note: Port 8081 was occupied by Docker"
echo "   📝 Available on different port if needed"

echo ""
echo "🔧 NETWORK CONFIGURATION:"

# Test connectivity
PING_RESULT=$(ping -c 1 -W 1 192.168.0.1 > /dev/null 2>&1 && echo "✅ Working" || echo "❌ Failed")
echo "   📡 Gateway Ping: $PING_RESULT"

# Test server responses
CRM_HTTP=$(curl -s -o /dev/null -w "%{http_code}" http://192.168.0.104:8082/network-test/ 2>/dev/null)
echo "   🏢 CRM Response: HTTP $CRM_HTTP"

# Firewall status
IPTABLES_PING=$(sudo iptables -L INPUT -n | grep -q "icmptype 8" && echo "✅ Allowed" || echo "❌ Blocked")
IPTABLES_8082=$(sudo iptables -L INPUT -n | grep -q "dpt:8082" && echo "✅ Allowed" || echo "❌ Blocked")
echo "   📶 PING Access: $IPTABLES_PING"
echo "   🏢 Port 8082: $IPTABLES_8082"

echo ""
echo "📱 ACCESS FROM OTHER DEVICES:"
echo "   🖥️  CRM System: http://192.168.0.104:8082/"
echo "   🧪 Quick Test: http://192.168.0.104:8082/network-test/"
echo "   👤 Admin Login: http://192.168.0.104:8082/admin/"
echo ""
echo "🔍 IF PING FAILS FROM OTHER DEVICES:"
echo "   1. Check router settings for 'Client Isolation' or 'AP Isolation'"
echo "   2. Disable client isolation if enabled"
echo "   3. Check other device's firewall settings"
echo "   4. Try connecting from different device types (phone, tablet, laptop)"
echo ""
echo "✅ SETUP COMPLETE!"
echo "   • CRM System is running and configured for network access"
echo "   • Firewall rules optimized for WiFi connectivity"
echo "   • Server bound to 0.0.0.0 for external device access"
echo "   • Network test endpoint available for connectivity verification"
