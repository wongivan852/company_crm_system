#!/usr/bin/env python3

"""
Restore Missing Customers from Complete Dataset
Adds missing customers to reach the original 1010+ count without backend changes
"""

import os
import sys
import django
import csv
import uuid
from datetime import datetime

# Setup Django
sys.path.append('/home/user/krystal-company-apps/company_crm_system/crm_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqlite_settings')
django.setup()

from crm.models import Customer
from django.db import transaction


def restore_missing_customers():
    """Restore missing customers from complete dataset"""
    
    print("=" * 60)
    print("    RESTORING MISSING CUSTOMERS")
    print("=" * 60)
    
    # Current state
    current_total = Customer.objects.count()
    current_youtube = Customer.objects.filter(customer_type='youtuber').count()
    current_regular = current_total - current_youtube
    
    print(f"📊 Current Database State:")
    print(f"   • Total: {current_total}")
    print(f"   • Regular: {current_regular}")
    print(f"   • YouTube: {current_youtube}")
    print()
    
    # Read complete dataset
    complete_csv = '/home/user/krystal-company-apps/company_crm_system/complete_customer_dataset_20250820_035231.csv'
    
    print(f"📁 Reading complete dataset: {complete_csv}")
    
    imported = 0
    skipped = 0
    errors = 0
    
    with open(complete_csv, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, 1):
            try:
                # Extract customer data
                customer_id = row.get('id', '').strip()
                first_name = row.get('first_name', '').strip()
                last_name = row.get('last_name', '').strip()
                email = row.get('email_primary', '').strip()
                customer_type = row.get('customer_type', '').strip()
                youtube_handle = row.get('youtube_handle', '').strip()
                company = row.get('company_primary', '').strip()
                
                # Skip if missing essential data
                if not first_name and not last_name and not email and not youtube_handle:
                    continue
                
                # Check if customer already exists by multiple criteria
                existing = None
                
                # Check by YouTube handle first
                if youtube_handle:
                    existing = Customer.objects.filter(youtube_handle__iexact=youtube_handle).first()
                
                # Check by email if no YouTube match
                if not existing and email:
                    existing = Customer.objects.filter(email_primary=email).first()
                
                # Check by UUID if provided
                if not existing and customer_id:
                    try:
                        existing = Customer.objects.filter(id=customer_id).first()
                    except:
                        pass
                
                # Check by name combination
                if not existing and first_name and last_name:
                    existing = Customer.objects.filter(
                        first_name__iexact=first_name,
                        last_name__iexact=last_name
                    ).first()
                
                if existing:
                    skipped += 1
                    continue
                
                # Create missing customer
                customer_data = {
                    'first_name': first_name or 'Unknown',
                    'last_name': last_name or 'Customer',
                    'email_primary': email if email and '@' in email else None,
                    'customer_type': customer_type or 'individual',
                    'status': row.get('status', '').strip() or 'active',
                    'company_primary': company,
                    'phone_primary': row.get('phone_primary', '').strip(),
                    'country_region': row.get('country_region', '').strip(),
                    'source': row.get('source', '').strip() or 'csv_restore',
                    'preferred_communication_method': row.get('preferred_communication_method', '').strip() or 'email',
                    'marketing_consent': row.get('marketing_consent', '').strip().lower() == 'true'
                }
                
                # Add YouTube specific fields
                if youtube_handle:
                    customer_data['youtube_handle'] = youtube_handle
                    customer_data['youtube_channel_url'] = row.get('youtube_channel_url', '').strip() or f"https://youtube.com/@{youtube_handle}"
                
                # Add social media fields
                if row.get('linkedin_profile'):
                    customer_data['linkedin_profile'] = row.get('linkedin_profile', '').strip()
                if row.get('twitter_handle'):
                    customer_data['twitter_handle'] = row.get('twitter_handle', '').strip()
                if row.get('instagram_handle'):
                    customer_data['instagram_handle'] = row.get('instagram_handle', '').strip()
                
                # Create customer
                with transaction.atomic():
                    customer = Customer(**customer_data)
                    customer.full_clean()
                    customer.save()
                    
                    imported += 1
                    print(f"Row {row_num}: Restored {customer_type} - {first_name} {last_name}")
                    
            except Exception as e:
                errors += 1
                print(f"Row {row_num}: Error - {str(e)}")
                continue
    
    # Final state
    final_total = Customer.objects.count()
    final_youtube = Customer.objects.filter(customer_type='youtuber').count()
    final_regular = final_total - final_youtube
    
    print()
    print("=" * 60)
    print("    RESTORATION COMPLETE")
    print("=" * 60)
    print(f"📊 Import Results:")
    print(f"   • Imported: {imported}")
    print(f"   • Skipped: {skipped}")
    print(f"   • Errors: {errors}")
    print()
    print(f"📈 Final Database State:")
    print(f"   • Total: {final_total}")
    print(f"   • Regular: {final_regular}")
    print(f"   • YouTube: {final_youtube}")
    print()
    
    if final_total >= 1010:
        print("✅ SUCCESS: Reached target of 1010+ customers!")
    else:
        print(f"⚠️  Still missing {1010 - final_total} customers")
    
    print("=" * 60)


if __name__ == '__main__':
    restore_missing_customers()
