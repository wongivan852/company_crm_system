#!/usr/bin/env python3
"""
UAT Readiness Check Script
Performs comprehensive checks to ensure the CRM system is ready for UAT
"""

import os
import sys
import django
import requests
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth.models import User
from crm.models import Customer
from django.db import connection

def check_database_connection():
    """Check if database is accessible"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection: OK")
        return True
    except Exception as e:
        print(f"❌ Database connection: FAILED - {e}")
        return False

def check_migrations():
    """Check if all migrations are applied"""
    try:
        from django.core.management.commands import migrate
        from io import StringIO
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        execute_from_command_line(['manage.py', 'showmigrations', '--plan'])
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        if '[X]' in output and '[ ]' not in output:
            print("✅ Database migrations: All applied")
            return True
        else:
            print("❌ Database migrations: Pending migrations found")
            print(output)
            return False
    except Exception as e:
        print(f"❌ Database migrations: ERROR - {e}")
        return False

def check_customer_model():
    """Test Customer model operations"""
    try:
        # Test model creation
        count_before = Customer.objects.count()
        
        # Test field access
        if count_before > 0:
            customer = Customer.objects.first()
            # Test all critical fields
            fields_to_test = [
                'first_name', 'last_name', 'email_primary', 'customer_type',
                'company_primary', 'phone_primary', 'created_at'
            ]
            
            for field in fields_to_test:
                getattr(customer, field)
        
        print(f"✅ Customer model: OK ({count_before} customers)")
        return True
    except Exception as e:
        print(f"❌ Customer model: FAILED - {e}")
        return False

def check_admin_access():
    """Check if admin user exists"""
    try:
        admin_count = User.objects.filter(is_superuser=True).count()
        if admin_count > 0:
            print(f"✅ Admin access: OK ({admin_count} superuser(s))")
            return True
        else:
            print("⚠️  Admin access: No superuser found")
            return False
    except Exception as e:
        print(f"❌ Admin access: ERROR - {e}")
        return False

def check_server_endpoints():
    """Check if key endpoints are responding"""
    base_url = "http://127.0.0.1:8001"
    endpoints = [
        "/",
        "/admin/", 
        "/customers/export/csv/",
        "/api/v1/"
    ]
    
    all_ok = True
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code in [200, 302, 403]:  # 403 is expected for protected endpoints
                print(f"✅ Endpoint {endpoint}: OK (Status: {response.status_code})")
            else:
                print(f"❌ Endpoint {endpoint}: FAILED (Status: {response.status_code})")
                all_ok = False
        except requests.exceptions.RequestException as e:
            print(f"❌ Endpoint {endpoint}: CONNECTION FAILED - {e}")
            all_ok = False
    
    return all_ok

def main():
    print("🔍 CRM System UAT Readiness Check")
    print("=" * 50)
    
    checks = [
        ("Database Connection", check_database_connection),
        ("Database Migrations", check_migrations),
        ("Customer Model", check_customer_model),
        ("Admin Access", check_admin_access),
        ("Server Endpoints", check_server_endpoints),
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        print(f"\n🔎 Checking {check_name}...")
        if check_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 UAT Readiness Score: {passed}/{total}")
    
    if passed == total:
        print("🎉 System is READY for UAT!")
        print("\n📋 Next Steps:")
        print("1. Access the application at: http://127.0.0.1:8001/")
        print("2. Test customer creation and data entry")
        print("3. Test CSV export functionality")
        print("4. Test admin interface at: http://127.0.0.1:8001/admin/")
        return True
    else:
        print("⚠️  System has issues that need to be resolved before UAT")
        return False

if __name__ == "__main__":
    main()
