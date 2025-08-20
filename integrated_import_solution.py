#!/usr/bin/env python3
"""
Integrated Import Solution for CRM System
Handles both regular customers and YouTube creators with minimal backend changes
"""

import os
import sys
import django
import csv
import re
from decimal import Decimal

# Setup Django
sys.path.append('/home/user/krystal-company-apps/company_crm_system/crm_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
django.setup()

from crm.models import Customer
from django.db import transaction
from django.core.exceptions import ValidationError


class IntegratedCRMImporter:
    """Handles importing both regular customers and YouTube creators"""
    
    def __init__(self):
        self.stats = {
            'regular_imported': 0,
            'regular_skipped': 0,
            'regular_errors': 0,
            'youtube_imported': 0,
            'youtube_skipped': 0,
            'youtube_errors': 0
        }
    
    def import_regular_customers(self, csv_file):
        """Import regular customers from master_eDM_list CSV"""
        print(f"Importing regular customers from: {csv_file}")
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row_num, row in enumerate(reader, 1):
                try:
                    # Extract and clean data
                    email = row.get('primary_email', '').strip()
                    first_name = row.get('first_name', '').strip()
                    last_name = row.get('last_name', '').strip()
                    company = row.get('company_primary', '').strip()
                    referral_source = row.get('referral_source', '').strip()
                    
                    # Skip if missing essential data
                    if not email or not (first_name or last_name):
                        print(f"Row {row_num}: Skipping - missing email or name")
                        self.stats['regular_skipped'] += 1
                        continue
                    
                    # Check if customer already exists
                    existing = Customer.objects.filter(email_primary=email).first()
                    if existing:
                        print(f"Row {row_num}: Skipping existing customer: {email}")
                        self.stats['regular_skipped'] += 1
                        continue
                    
                    # Determine customer type
                    customer_type = self._determine_customer_type(company, email)
                    
                    # Create customer data
                    customer_data = {
                        'first_name': first_name,
                        'last_name': last_name or 'Customer',
                        'email_primary': email,
                        'company_primary': company,
                        'customer_type': customer_type,
                        'status': 'active',
                        'preferred_communication_method': 'email',
                        'source': 'website',
                        'referral_source': referral_source or 'csv_import',
                        'marketing_consent': True,
                        'data_processing_consent': True
                    }
                    
                    # Create and save customer
                    with transaction.atomic():
                        customer = Customer(**customer_data)
                        customer.full_clean()
                        customer.save()
                        
                        print(f"Row {row_num}: Created {customer_type} - {first_name} {last_name} ({email})")
                        self.stats['regular_imported'] += 1
                
                except Exception as e:
                    print(f"Row {row_num}: Error - {str(e)}")
                    self.stats['regular_errors'] += 1
                    continue
    
    def import_youtube_creators(self, csv_file):
        """Import YouTube creators with enhanced handling"""
        print(f"Importing YouTube creators from: {csv_file}")
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row_num, row in enumerate(reader, 1):
                try:
                    # Extract YouTube-specific data
                    youtube_handle = row.get('YouTube Handle', '').strip().lstrip('@')
                    youtube_url = row.get('YouTube Channel URL', '').strip()
                    first_name = row.get('First Name', '').strip()
                    last_name = row.get('Last Name', '').strip()
                    email = row.get('Primary Email', '').strip()
                    company = row.get('Primary Company', '').strip()
                    
                    # Skip if no YouTube handle
                    if not youtube_handle:
                        print(f"Row {row_num}: Skipping - no YouTube handle")
                        self.stats['youtube_skipped'] += 1
                        continue
                    
                    # Check if YouTube creator already exists
                    existing = Customer.objects.filter(youtube_handle__iexact=youtube_handle).first()
                    if existing:
                        print(f"Row {row_num}: Skipping existing YouTuber: @{youtube_handle}")
                        self.stats['youtube_skipped'] += 1
                        continue
                    
                    # Generate names if missing
                    if not first_name and not last_name:
                        name_parts = self._parse_name_from_handle(youtube_handle)
                        first_name = name_parts[0]
                        last_name = name_parts[1]
                    elif not first_name:
                        first_name = youtube_handle.title()
                    elif not last_name:
                        last_name = 'Creator'
                    
                    # Generate YouTube URL if missing
                    if not youtube_url:
                        youtube_url = f"https://youtube.com/@{youtube_handle}"
                    
                    # Create YouTube creator data
                    customer_data = {
                        'first_name': first_name,
                        'last_name': last_name,
                        'email_primary': email if email and '@' in email else None,
                        'customer_type': 'youtuber',
                        'status': 'prospect',
                        'youtube_handle': youtube_handle,
                        'youtube_channel_url': youtube_url,
                        'company_primary': company or f"{first_name} {last_name} Channel",
                        'position_primary': 'Content Creator',
                        'preferred_communication_method': 'email' if email else 'whatsapp',
                        'source': 'youtube_import',
                        'referral_source': 'csv_import',
                        'interests': 'Content Creation, Video Production',
                        'marketing_consent': False,  # Need explicit consent for YouTubers
                        'data_processing_consent': True
                    }
                    
                    # Create and save YouTube creator
                    with transaction.atomic():
                        customer = Customer(**customer_data)
                        customer.full_clean()
                        customer.save()
                        
                        print(f"Row {row_num}: Created YouTuber @{youtube_handle} - {first_name} {last_name}")
                        self.stats['youtube_imported'] += 1
                
                except Exception as e:
                    print(f"Row {row_num}: Error - {str(e)}")
                    self.stats['youtube_errors'] += 1
                    continue
    
    def _determine_customer_type(self, company, email):
        """Determine customer type based on company and email"""
        if not company:
            return 'individual'
        
        company_lower = company.lower()
        email_lower = email.lower() if email else ''
        
        # Check for educational institutions
        if any(keyword in company_lower for keyword in ['university', 'school', 'college', 'institute', 'academy']):
            return 'student'
        
        # Check for educational email domains
        if any(domain in email_lower for domain in ['.edu', '.ac.', 'student.']):
            return 'student'
        
        # Check for corporate indicators
        if any(keyword in company_lower for keyword in ['inc', 'ltd', 'corp', 'company', 'llc', 'studio', 'agency']):
            return 'corporate'
        
        # Default to individual
        return 'individual'
    
    def _parse_name_from_handle(self, handle):
        """Parse first and last name from YouTube handle"""
        # Try to split CamelCase or underscore handle
        name_parts = re.findall(r'[A-Z][a-z]*|[a-z]+', handle.replace('_', ' ').replace('-', ' '))
        
        if name_parts:
            first_name = name_parts[0].title()
            if len(name_parts) > 1:
                last_name = ' '.join(name_parts[1:]).title()
            else:
                last_name = 'Creator'
        else:
            first_name = handle.title()
            last_name = 'Creator'
        
        return [first_name, last_name]
    
    def clear_youtube_only_data(self):
        """Clear existing YouTube-only data if needed"""
        youtube_count = Customer.objects.filter(customer_type='youtuber').count()
        if youtube_count > 0:
            response = input(f"Found {youtube_count} existing YouTube creators. Clear them? (y/N): ")
            if response.lower() == 'y':
                Customer.objects.filter(customer_type='youtuber').delete()
                print(f"Cleared {youtube_count} YouTube creators")
    
    def print_summary(self):
        """Print import summary"""
        print("\n" + "="*60)
        print("IMPORT SUMMARY")
        print("="*60)
        print(f"Regular Customers:")
        print(f"  - Imported: {self.stats['regular_imported']}")
        print(f"  - Skipped:  {self.stats['regular_skipped']}")
        print(f"  - Errors:   {self.stats['regular_errors']}")
        print(f"\nYouTube Creators:")
        print(f"  - Imported: {self.stats['youtube_imported']}")
        print(f"  - Skipped:  {self.stats['youtube_skipped']}")
        print(f"  - Errors:   {self.stats['youtube_errors']}")
        
        # Final counts
        total_customers = Customer.objects.count()
        youtube_customers = Customer.objects.filter(customer_type='youtuber').count()
        regular_customers = total_customers - youtube_customers
        
        print(f"\nFinal Database State:")
        print(f"  - Total Customers: {total_customers}")
        print(f"  - Regular Customers: {regular_customers}")
        print(f"  - YouTube Creators: {youtube_customers}")
        print("="*60)


def main():
    """Main import function"""
    importer = IntegratedCRMImporter()
    
    # Paths to CSV files
    base_dir = '/home/user/krystal-company-apps/company_crm_system'
    regular_csv = os.path.join(base_dir, 'master_eDM_list - Polished CRM import.csv')
    youtube_csv = os.path.join(base_dir, 'youtube_creators_import.csv')
    
    print("Integrated CRM Import Solution")
    print("="*50)
    
    # Check current state
    current_total = Customer.objects.count()
    current_youtube = Customer.objects.filter(customer_type='youtuber').count()
    current_regular = current_total - current_youtube
    
    print(f"Current Database State:")
    print(f"  - Total: {current_total}")
    print(f"  - Regular: {current_regular}")
    print(f"  - YouTube: {current_youtube}")
    print()
    
    # Import regular customers if needed
    if current_regular == 0 and os.path.exists(regular_csv):
        print("Importing missing regular customers...")
        importer.import_regular_customers(regular_csv)
    else:
        print("Regular customers already imported or CSV not found")
    
    # Import YouTube creators (merge with existing if any)
    if os.path.exists(youtube_csv):
        print("\nImporting YouTube creators...")
        importer.import_youtube_creators(youtube_csv)
    else:
        print("YouTube CSV not found")
    
    # Print final summary
    importer.print_summary()


if __name__ == '__main__':
    main()
