#!/usr/bin/env python
"""
Custom Country-Aware Import Script for CRM Data
Handles country name to country code mapping properly
"""
import os
import sys
import csv
import logging
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')

import django
django.setup()

from crm.models import Customer
from django.db import transaction
from django.core.exceptions import ValidationError

# Country mapping from full names to model codes
COUNTRY_MAPPING = {
    'hong kong sar': 'HK',
    'hong kong': 'HK',
    'china': 'CN',
    'south korea': 'KR',
    'nigeria': 'NG',
    'united kingdom': 'GB',
    'uk': 'GB',
    'other (please specify in notes)': 'OTHER',
    'india': 'IN',
    'philippines': 'PH',
    'france': 'FR',
    'japan': 'JP',
    'thailand': 'TH',
    'malaysia': 'MY',
    'taiwan': 'TW',
    'united states': 'US',
    'usa': 'US',
    'peru': 'PE',
    'switzerland': 'CH',
    'italy': 'IT',
    'south africa': 'ZA',
    'netherlands': 'NL',
    'australia': 'AU',
    'canada': 'CA',
    'singapore': 'SG',
    'germany': 'DE',
    'brazil': 'BR',
    'mexico': 'MX',
    # Add existing codes that are already correct
    'HK': 'HK',
    'CN': 'CN',
    'KR': 'KR',
    'NG': 'NG',
    'GB': 'GB',
    'IN': 'IN',
    'PH': 'PH',
    'FR': 'FR',
    'JP': 'JP',
    'TH': 'TH',
    'MY': 'MY',
    'TW': 'TW',
    'US': 'US',
    'PE': 'PE',
    'CH': 'CH',
    'IT': 'IT',
    'ZA': 'ZA',
    'NL': 'NL',
    'AU': 'AU',
    'CA': 'CA',
    'SG': 'SG',
    'DE': 'DE',
    'BR': 'BR',
    'MX': 'MX',
}

def map_country(country_name):
    """Map country name to country code"""
    if not country_name or not country_name.strip():
        return ''
    
    country_key = country_name.strip().lower()
    mapped_code = COUNTRY_MAPPING.get(country_key, '')
    
    if not mapped_code and country_name.strip():
        print(f"⚠️ Unknown country: '{country_name}' - will be left empty")
    
    return mapped_code

def clean_field(value):
    """Clean field value"""
    if not value:
        return ''
    return str(value).strip()

def import_customers_with_country_mapping(csv_file):
    """Import customers with proper country mapping"""
    print(f"🚀 Starting import from {csv_file}")
    
    success_count = 0
    error_count = 0
    duplicate_count = 0
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row_num, row in enumerate(reader, start=1):
            try:
                with transaction.atomic():
                    # Extract and clean data
                    first_name = clean_field(row.get('first_name', ''))
                    last_name = clean_field(row.get('last_name', ''))
                    email_primary = clean_field(row.get('email_primary', ''))
                    
                    # Map country
                    country_raw = clean_field(row.get('country_region', ''))
                    country_region = map_country(country_raw)
                    
                    # Check for duplicates based on email
                    if email_primary and Customer.objects.filter(email_primary=email_primary).exists():
                        duplicate_count += 1
                        print(f"⚠️ Row {row_num}: Duplicate email {email_primary}")
                        continue
                    
                    # Create customer data
                    customer_data = {
                        'first_name': first_name,
                        'last_name': last_name,
                        'email_primary': email_primary,
                        'email_secondary': clean_field(row.get('email_secondary', '')),
                        'phone_primary': clean_field(row.get('phone_primary', '')),
                        'phone_secondary': clean_field(row.get('phone_secondary', '')),
                        'company_name': clean_field(row.get('company_name', '')),
                        'job_title': clean_field(row.get('job_title', '')),
                        'industry': clean_field(row.get('industry', '')),
                        'customer_type': clean_field(row.get('customer_type', 'corporate')),
                        'lead_status': clean_field(row.get('lead_status', 'new')),
                        'source': clean_field(row.get('source', 'import')),
                        'country_region': country_region,
                        'address_line1': clean_field(row.get('address_line1', '')),
                        'address_line2': clean_field(row.get('address_line2', '')),
                        'city': clean_field(row.get('city', '')),
                        'state_province': clean_field(row.get('state_province', '')),
                        'postal_code': clean_field(row.get('postal_code', '')),
                        'website': clean_field(row.get('website', '')),
                        'notes': clean_field(row.get('notes', '')),
                        'youtube_handle': clean_field(row.get('youtube_handle', '')),
                        'instagram_handle': clean_field(row.get('instagram_handle', '')),
                        'twitter_handle': clean_field(row.get('twitter_handle', '')),
                        'facebook_page': clean_field(row.get('facebook_page', '')),
                        'linkedin_profile': clean_field(row.get('linkedin_profile', '')),
                        'tiktok_handle': clean_field(row.get('tiktok_handle', '')),
                    }
                    
                    # Create customer
                    customer = Customer(**customer_data)
                    customer.full_clean()  # Validate before save
                    customer.save()
                    
                    success_count += 1
                    if success_count % 100 == 0:
                        print(f"✅ Imported {success_count} customers...")
                    
            except ValidationError as e:
                error_count += 1
                print(f"❌ Row {row_num}: Validation error - {e}")
                
            except Exception as e:
                error_count += 1
                print(f"❌ Row {row_num}: Unexpected error - {e}")
    
    print(f"\n📊 IMPORT SUMMARY:")
    print(f"✅ Successful imports: {success_count}")
    print(f"⚠️ Duplicates skipped: {duplicate_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📋 Total processed: {success_count + duplicate_count + error_count}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_country_import.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    if not os.path.exists(csv_file):
        print(f"Error: File {csv_file} not found")
        sys.exit(1)
    
    import_customers_with_country_mapping(csv_file)
