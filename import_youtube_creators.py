#!/usr/bin/env python
"""
YouTube Creators Import Script
Safely imports YouTube creators without affecting existing data
"""
import os
import sys
import django
import csv
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
sys.path.append('/Users/wongivan/ai_tools/business_tools/company_crm_system/crm_project')
django.setup()

from crm.models import Customer

def import_youtube_creators():
    """Import YouTube creators from CSV"""
    csv_path = Path("youtube_creators_import.csv")
    
    if not csv_path.exists():
        print(f"File not found: {csv_path}")
        return
    
    imported = 0
    errors = 0
    duplicates = 0
    
    print("Starting YouTube creators import...")
    print("=" * 50)
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            try:
                # Extract data from CSV
                first_name = row.get('First Name', '').strip()
                last_name = row.get('Last Name', '').strip()
                email = row.get('Primary Email', '').strip() or None
                youtube_handle = row.get('YouTube Handle', '').strip()
                youtube_channel_url = row.get('YouTube Channel URL', '').strip()
                company = row.get('Primary Company', '').strip()
                customer_type = row.get('Customer Type', 'youtuber').strip()
                status = row.get('Status', 'prospect').strip()
                source = row.get('Source', 'youtube_import').strip()
                preferred_comm = row.get('Preferred Communication Method', 'email').strip()
                country = row.get('Country/Region', '').strip()
                position = row.get('Primary Position', '').strip()
                
                # Validate required data
                if not youtube_handle:
                    print(f"Skipping row: No YouTube handle provided")
                    continue
                
                # Clean YouTube handle
                youtube_handle = youtube_handle.lstrip('@')
                
                # Check for existing customer by YouTube handle
                existing_by_handle = Customer.objects.filter(youtube_handle__iexact=youtube_handle).first()
                if existing_by_handle:
                    print(f"Duplicate YouTube handle: @{youtube_handle} (existing customer: {existing_by_handle.first_name} {existing_by_handle.last_name})")
                    duplicates += 1
                    continue
                
                # Check for existing customer by email (if provided)
                if email:
                    existing_by_email = Customer.objects.filter(email_primary=email).first()
                    if existing_by_email:
                        print(f"Duplicate email: {email} (existing customer: {existing_by_email.first_name} {existing_by_email.last_name})")
                        duplicates += 1
                        continue
                
                # Create customer
                customer = Customer(
                    first_name=first_name or youtube_handle.replace('_', ' ').replace('.', ' ').title(),
                    last_name=last_name or 'Creator',
                    email_primary=email,
                    youtube_handle=youtube_handle,
                    youtube_channel_url=youtube_channel_url,
                    company_primary=company,
                    customer_type=customer_type,
                    status=status,
                    source=source,
                    preferred_communication_method=preferred_comm,
                    country_region=country,
                    position_primary=position,
                )
                
                # Save and let the model handle validation and auto-generation
                customer.save()
                imported += 1
                
                print(f"✓ Imported: @{youtube_handle} - {customer.first_name} {customer.last_name}")
                
                if imported % 10 == 0:
                    print(f"Progress: {imported} creators imported...")
                    
            except Exception as e:
                errors += 1
                print(f"✗ Error importing @{youtube_handle}: {e}")
                continue
    
    print(f"\nImport Summary:")
    print(f"=" * 50)
    print(f"✓ Successfully imported: {imported} YouTube creators")
    print(f"⚠ Duplicates skipped: {duplicates}")
    print(f"✗ Errors encountered: {errors}")
    print(f"📊 Total YouTube creators in database: {Customer.objects.filter(customer_type='youtuber').count()}")

def test_youtube_import():
    """Test import with a single record"""
    print("Testing YouTube import with sample data...")
    
    # Test if we can create a YouTube customer
    test_handle = "test_youtuber_import"
    
    # Clean up any existing test data
    Customer.objects.filter(youtube_handle=test_handle).delete()
    
    try:
        customer = Customer(
            first_name="Test",
            last_name="YouTuber",
            youtube_handle=test_handle,
            customer_type="youtuber",
            status="prospect",
            source="test_import"
        )
        customer.save()
        
        print(f"✓ Test successful: Created {customer.first_name} {customer.last_name} (@{customer.youtube_handle})")
        print(f"  - Auto-generated email: {customer.email_primary}")
        print(f"  - Auto-generated URL: {customer.youtube_channel_url}")
        
        # Clean up test data
        customer.delete()
        print(f"✓ Test cleanup completed")
        
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

if __name__ == "__main__":
    # First run a test
    if test_youtube_import():
        print(f"\n" + "=" * 50)
        print("Test passed. Proceeding with full import...")
        print("=" * 50)
        
        # Run the actual import
        import_youtube_creators()
    else:
        print("Test failed. Please check the system configuration.")