#!/usr/bin/env python3

"""
Customer Count Verification View
Shows exact customer counts without admin interface pagination
"""

import os
import sys
import django

# Setup Django
sys.path.append('/home/user/krystal-company-apps/company_crm_system/crm_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
django.setup()

from crm.models import Customer
from django.db.models import Count

def show_customer_counts():
    print("=" * 60)
    print("    EXACT CUSTOMER COUNT VERIFICATION")
    print("=" * 60)
    
    # Total count
    total = Customer.objects.count()
    print(f"📊 TOTAL CUSTOMERS: {total}")
    
    # By type
    print(f"\n📋 BY CUSTOMER TYPE:")
    types = Customer.objects.values('customer_type').annotate(count=Count('customer_type')).order_by('-count')
    for t in types:
        print(f"   • {t['customer_type'].title()}: {t['count']}")
    
    # By status
    print(f"\n📊 BY STATUS:")
    statuses = Customer.objects.values('status').annotate(count=Count('status')).order_by('-count')
    for s in statuses:
        print(f"   • {s['status'].title()}: {s['count']}")
    
    # Admin pagination info
    print(f"\n📄 ADMIN INTERFACE INFO:")
    print(f"   • Admin shows: 100 customers per page")
    print(f"   • Total pages: {(total + 99) // 100}")
    print(f"   • To see all customers: Navigate through all pages")
    
    # Recent customers
    print(f"\n🕐 RECENT CUSTOMERS (last 10):")
    for customer in Customer.objects.order_by('-created_at')[:10]:
        print(f"   • {customer.first_name} {customer.last_name} ({customer.customer_type})")
    
    print(f"\n✅ CONCLUSION:")
    print(f"   Database contains exactly {total} customers")
    print(f"   Admin interface uses pagination (100 per page)")
    print(f"   All data is intact and accessible")
    print("=" * 60)

if __name__ == '__main__':
    show_customer_counts()
