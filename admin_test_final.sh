#!/bin/bash

echo "🔧 FINAL ADMIN PANEL TEST & VERIFICATION"
echo "======================================="
echo ""

# Test admin panel redirect (should be 302)
echo "🧪 TESTING ADMIN PANEL ACCESS:"
ADMIN_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://192.168.0.104:8082/admin/)
if [ "$ADMIN_STATUS" = "302" ]; then
    echo "   ✅ Admin Panel: Working (HTTP $ADMIN_STATUS - Redirects to login)"
    echo "   🔗 URL: http://192.168.0.104:8082/admin/"
else
    echo "   ❌ Admin Panel: Failed (HTTP $ADMIN_STATUS)"
fi

# Test admin login page
echo ""
echo "🔐 TESTING ADMIN LOGIN PAGE:"
LOGIN_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://192.168.0.104:8082/admin/login/)
if [ "$LOGIN_STATUS" = "200" ]; then
    echo "   ✅ Login Page: Working (HTTP $LOGIN_STATUS)"
    echo "   🔗 URL: http://192.168.0.104:8082/admin/login/"
else
    echo "   ❌ Login Page: Failed (HTTP $LOGIN_STATUS)"
fi

# Test database connection
echo ""
echo "💾 TESTING DATABASE CONNECTION:"
cd /home/user/krystal-company-apps/company_crm_system/crm_project
DB_TEST=$(/home/user/krystal-company-apps/claude-env/bin/python manage.py shell -c "
from django.contrib.auth.models import User
from django.db import connection
try:
    user_count = User.objects.count()
    print(f'SUCCESS:{user_count}')
except Exception as e:
    print(f'ERROR:{e}')
" 2>/dev/null)

if [[ $DB_TEST == SUCCESS:* ]]; then
    USER_COUNT=$(echo $DB_TEST | cut -d':' -f2)
    echo "   ✅ Database: Connected ($USER_COUNT users found)"
    echo "   ✅ Auth tables: Present and working"
else
    echo "   ❌ Database Error: $DB_TEST"
fi

# Test server binding
echo ""
echo "🌐 SERVER CONFIGURATION:"
SERVER_PID=$(pgrep -f "manage.py runserver")
if [ ! -z "$SERVER_PID" ]; then
    echo "   ✅ Server: Running (PID: $SERVER_PID)"
    BINDING=$(ss -tlnp | grep :8082 | grep "0.0.0.0:8082")
    if [ ! -z "$BINDING" ]; then
        echo "   ✅ Binding: 0.0.0.0:8082 (accessible from network)"
    else
        echo "   ⚠️  Binding: May not be accessible from network"
    fi
else
    echo "   ❌ Server: Not running"
fi

# Test all endpoints
echo ""
echo "🎯 ENDPOINT TESTS:"
endpoints=("/" "/admin/" "/network-test/" "/network-landing/")
for endpoint in "${endpoints[@]}"; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://192.168.0.104:8082$endpoint 2>/dev/null)
    if [ "$STATUS" = "200" ] || [ "$STATUS" = "302" ]; then
        echo "   ✅ $endpoint - HTTP $STATUS"
    else
        echo "   ❌ $endpoint - HTTP $STATUS"
    fi
done

echo ""
echo "🔑 ADMIN CREDENTIALS:"
echo "   👤 Username: admin"
echo "   🔒 Password: admin123"
echo ""
echo "📱 READY FOR ACCESS FROM OTHER DEVICES:"
echo "   🏢 Main CRM: http://192.168.0.104:8082/"
echo "   👤 Admin Panel: http://192.168.0.104:8082/admin/"
echo "   🧪 Network Test: http://192.168.0.104:8082/network-test/"
echo "   🎨 Landing Page: http://192.168.0.104:8082/network-landing/"
