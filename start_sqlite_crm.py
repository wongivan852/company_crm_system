#!/usr/bin/env python3

"""
Direct SQLite CRM Startup
Bypasses .env configuration and forces SQLite usage
"""

import os
import sys
import django
from django.conf import settings

# Set project path
project_path = '/home/user/krystal-company-apps/company_crm_system/crm_project'
sys.path.insert(0, project_path)

# Configure Django settings directly
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')

# Override database to use SQLite
os.environ['DATABASE_URL'] = 'sqlite:////home/user/krystal-company-apps/company_crm_system/crm_test_safe.sqlite3'
os.environ['DEBUG'] = '1'
os.environ['SECRET_KEY'] = 'direct-sqlite-key'
os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1,0.0.0.0,*'
os.environ['SECURE_SSL_REDIRECT'] = '0'
os.environ['SESSION_COOKIE_SECURE'] = '0'
os.environ['CSRF_COOKIE_SECURE'] = '0'

# Change to project directory
os.chdir(project_path)

# Setup Django
django.setup()

print("=" * 60)
print("          DIRECT SQLITE CRM ACCESS")
print("=" * 60)

# Test database
try:
    from crm.models import Customer
    total = Customer.objects.count()
    youtube = Customer.objects.filter(customer_type='youtuber').count()
    regular = total - youtube
    
    print(f"✅ Database Connection: SUCCESS")
    print(f"📊 Customer Data:")
    print(f"   • Total Customers: {total}")
    print(f"   • Regular Customers: {regular}")
    print(f"   • YouTube Creators: {youtube}")
    print()
    print(f"🌐 Access URLs:")
    print(f"   • Main App: http://localhost:8888/")
    print(f"   • Admin: http://localhost:8888/admin/")
    print(f"   • API: http://localhost:8888/api/")
    print()
    print(f"👤 Admin Login: admin / admin123")
    print()
    print("🚀 Starting server...")
    print("=" * 60)
    
    # Start server
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8888', '--insecure'])
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTrying alternative database path...")
    try:
        # Try alternative database path
        os.environ['DATABASE_URL'] = 'sqlite:////home/user/krystal-company-apps/company_crm_system/updated.db'
        django.setup()
        from crm.models import Customer
        total = Customer.objects.count()
        print(f"✅ Alternative database working with {total} customers")
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8888', '--insecure'])
    except Exception as e2:
        print(f"❌ Alternative also failed: {e2}")
