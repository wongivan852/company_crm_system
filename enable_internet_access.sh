#!/bin/bash

echo "🔥 ENABLING INTERNET ACCESS FOR CRM"
echo "=================================="

echo "Configuring UFW firewall..."
sudo ufw allow 8082/tcp comment 'CRM System Internet Access'
sudo ufw allow ssh
sudo ufw reload

echo ""
echo "✅ Firewall configured!"
echo ""
echo "Testing external access..."
sleep 2
curl -I http://203.186.246.162:8082/ 2>/dev/null | head -3 || echo "Still blocked - may need router configuration"

echo ""
echo "🌐 Your CRM should now be accessible at:"
echo "   http://203.186.246.162:8082/"
echo "   http://203.186.246.162:8082/admin/"
echo ""
echo "👤 Login: admin / admin123"
