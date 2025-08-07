#!/bin/bash

echo "🔍 COMPREHENSIVE NETWORK DIAGNOSTIC FOR CRM SYSTEM"
echo "=================================================="
echo ""

# Server status
echo "📊 SERVER STATUS:"
SERVER_PID=$(pgrep -f "manage.py runserver")
if [ ! -z "$SERVER_PID" ]; then
    echo "✅ CRM Server running (PID: $SERVER_PID)"
else
    echo "❌ CRM Server not running"
fi

# Network interfaces
echo ""
echo "🌐 NETWORK INTERFACES:"
ip addr show | grep -E "inet.*192\.|inet.*10\.|inet.*172\." | while read line; do
    echo "   $line"
done

# Active connections
echo ""
echo "🔗 ACTIVE NETWORK CONNECTIONS:"
nmcli connection show --active | while read line; do
    echo "   $line"
done

# Gateway connectivity
echo ""
echo "🛣️  GATEWAY CONNECTIVITY:"
GATEWAY=$(ip route | grep default | awk '{print $3}' | head -1)
ping -c 1 -W 1 $GATEWAY > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Gateway reachable: $GATEWAY"
else
    echo "❌ Gateway unreachable: $GATEWAY"
fi

# Port status
echo ""
echo "🔌 PORT 8082 STATUS:"
netstat -tlnp | grep :8082 | while read line; do
    echo "   $line"
done

# Server response tests
echo ""
echo "🧪 SERVER RESPONSE TESTS:"
for ip in "127.0.0.1" "192.168.0.104"; do
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://$ip:8082 2>/dev/null)
    if [ "$RESPONSE" = "302" ] || [ "$RESPONSE" = "200" ]; then
        echo "✅ $ip:8082 - Working (HTTP $RESPONSE)"
    else
        echo "❌ $ip:8082 - Failed (HTTP $RESPONSE)"
    fi
done

# Iptables rules check
echo ""
echo "🛡️  IPTABLES RULES:"
sudo iptables -L -n | grep -E "(8082|REJECT|DROP)" | head -5 | while read line; do
    echo "   $line"
done

# Check for client isolation indicators
echo ""
echo "🔒 POTENTIAL CLIENT ISOLATION CHECKS:"
# Check if we can reach other common local IPs
ping -c 1 -W 1 192.168.0.1 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Router communication working"
else
    echo "❌ Router communication failed"
fi

# Check if server is binding correctly
echo ""
echo "📡 SERVER BINDING STATUS:"
ss -tulpn | grep :8082 | while read line; do
    echo "   $line"
done

echo ""
echo "🎯 DEBUGGING RESULTS SUMMARY:"
echo "   WiFi IP: 192.168.0.104"
echo "   Server: Running on 0.0.0.0:8082"
echo "   Local Access: Working"
echo ""
echo "📱 FOR OTHER DEVICE TESTING:"
echo "   1. From other device, try: ping 192.168.0.104"
echo "   2. If ping fails: Check router's client isolation settings"
echo "   3. If ping works but HTTP fails: Try curl -v http://192.168.0.104:8082"
echo "   4. Check other device's firewall settings"
echo ""
echo "⚡ QUICK FIXES TO TRY:"
echo "   1. Restart network: sudo systemctl restart NetworkManager"
echo "   2. Flush iptables: sudo iptables -F"
echo "   3. Check router admin panel for client isolation"
echo "   4. Try different port: python manage.py runserver 0.0.0.0:8083"
