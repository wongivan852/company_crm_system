#!/usr/bin/env python3

"""
Simple CRM Startup Script
Bypasses complex configuration and starts a working Django server
"""

import os
import sys
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')

# Add the project directory to Python path
project_dir = '/home/user/krystal-company-apps/company_crm_system/crm_project'
sys.path.insert(0, project_dir)

# Set environment variables for development
os.environ['DEBUG'] = '1'
os.environ['SECRET_KEY'] = 'simple-dev-key-not-for-production'
os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1,0.0.0.0,*'
os.environ['SECURE_SSL_REDIRECT'] = '0'
os.environ['SESSION_COOKIE_SECURE'] = '0'
os.environ['CSRF_COOKIE_SECURE'] = '0'
os.environ['DATABASE_URL'] = 'postgresql://crm_user:5514@localhost:5432/crm_db'

# Change to the Django project directory
os.chdir(project_dir)

# Setup Django
django.setup()

# Import Django management
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    print("=" * 60)
    print("          SIMPLE CRM STARTUP")
    print("=" * 60)
    
    # Check database connectivity
    try:
        from crm.models import Customer
        customer_count = Customer.objects.count()
        youtube_count = Customer.objects.filter(customer_type='youtuber').count()
        regular_count = customer_count - youtube_count
        
        print(f"📊 Database Status:")
        print(f"   • Total Customers: {customer_count}")
        print(f"   • Regular Customers: {regular_count}")
        print(f"   • YouTube Creators: {youtube_count}")
        print()
    except Exception as e:
        print(f"⚠️  Database connection issue: {e}")
        print()
    
    print("🌐 Starting server on http://localhost:8006/")
    print("🔑 Admin: http://localhost:8006/admin/ (admin/admin123)")
    print("📋 API: http://localhost:8006/api/")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    # Start the development server
    try:
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8006'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
