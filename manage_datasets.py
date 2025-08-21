#!/usr/bin/env python3
"""
Dataset Management Script for CRM System
Manages CSV datasets within the Docker environment
"""

import os
import sys
import csv
import glob
from pathlib import Path

# Add the Django project to the path
sys.path.append('/app/crm_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')

try:
    import django
    django.setup()
    from crm.models import Customer
    from django.db import transaction
except ImportError as e:
    print(f"Warning: Django not available: {e}")
    Customer = None

def list_datasets():
    """List all available datasets"""
    datasets_path = Path('/app/data/datasets')
    if not datasets_path.exists():
        print("❌ Datasets directory not found!")
        return []
    
    csv_files = list(datasets_path.glob('*.csv'))
    
    print(f"📊 Found {len(csv_files)} dataset(s):")
    for i, csv_file in enumerate(csv_files, 1):
        size_mb = csv_file.stat().st_size / (1024 * 1024)
        print(f"   {i}. {csv_file.name} ({size_mb:.1f} MB)")
        
        # Quick peek at the CSV structure
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                print(f"      📋 Columns: {len(header)} - {', '.join(header[:5])}{'...' if len(header) > 5 else ''}")
                
                # Count rows (approximation for large files)
                row_count = sum(1 for _ in reader)
                print(f"      📈 Rows: ~{row_count}")
        except Exception as e:
            print(f"      ⚠️  Could not read file: {e}")
        print()
    
    return csv_files

def validate_dataset(csv_file):
    """Validate a CSV dataset"""
    print(f"🔍 Validating {csv_file.name}...")
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            
            print(f"   📋 Headers: {headers}")
            
            # Read a few sample rows
            samples = []
            for i, row in enumerate(reader):
                if i >= 3:  # Only read first 3 rows as samples
                    break
                samples.append(row)
            
            print(f"   📊 Sample data ({len(samples)} rows):")
            for i, sample in enumerate(samples):
                print(f"      Row {i+1}: {dict(list(sample.items())[:3])}")  # Show first 3 columns
            
            return True, headers
            
    except Exception as e:
        print(f"   ❌ Validation failed: {e}")
        return False, None

def import_dataset_to_django(csv_file):
    """Import a dataset into Django CRM models"""
    if Customer is None:
        print("❌ Django models not available. Cannot import to database.")
        return False
    
    print(f"📥 Importing {csv_file.name} to Django CRM...")
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            imported_count = 0
            skipped_count = 0
            
            with transaction.atomic():
                for row in reader:
                    # Map CSV columns to Django model fields
                    # This is a simplified mapping - adjust based on your actual CSV structure
                    customer_data = {}
                    
                    # Common field mappings
                    field_mappings = {
                        'name': ['name', 'full_name', 'customer_name', 'Name'],
                        'email': ['email', 'email_address', 'Email'],
                        'phone': ['phone', 'phone_number', 'mobile', 'Phone'],
                        'company': ['company', 'organization', 'Company'],
                    }
                    
                    for model_field, possible_csv_fields in field_mappings.items():
                        for csv_field in possible_csv_fields:
                            if csv_field in row and row[csv_field]:
                                customer_data[model_field] = row[csv_field]
                                break
                    
                    # Skip if no email (assuming email is required)
                    if 'email' not in customer_data:
                        skipped_count += 1
                        continue
                    
                    # Create or update customer
                    customer, created = Customer.objects.get_or_create(
                        email=customer_data['email'],
                        defaults=customer_data
                    )
                    
                    if created:
                        imported_count += 1
                    else:
                        skipped_count += 1
            
            print(f"   ✅ Import complete:")
            print(f"      📈 Imported: {imported_count}")
            print(f"      ⏭️  Skipped: {skipped_count}")
            return True
            
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False

def main():
    """Main function"""
    print("🗄️  CRM Dataset Manager")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'list':
            list_datasets()
            
        elif command == 'validate':
            datasets = list_datasets()
            if len(sys.argv) > 2:
                filename = sys.argv[2]
                dataset_file = Path('/app/data/datasets') / filename
                if dataset_file.exists():
                    validate_dataset(dataset_file)
                else:
                    print(f"❌ File not found: {filename}")
            else:
                print("Usage: python manage_datasets.py validate <filename>")
                
        elif command == 'import':
            if len(sys.argv) > 2:
                filename = sys.argv[2]
                dataset_file = Path('/app/data/datasets') / filename
                if dataset_file.exists():
                    valid, headers = validate_dataset(dataset_file)
                    if valid:
                        import_dataset_to_django(dataset_file)
                    else:
                        print("❌ Cannot import invalid dataset")
                else:
                    print(f"❌ File not found: {filename}")
            else:
                print("Usage: python manage_datasets.py import <filename>")
                
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands: list, validate, import")
    else:
        # Default: list datasets
        list_datasets()
        
        # Show usage
        print("\n💡 Usage:")
        print("   python manage_datasets.py list              - List all datasets")
        print("   python manage_datasets.py validate <file>   - Validate a dataset")
        print("   python manage_datasets.py import <file>     - Import dataset to Django")

if __name__ == '__main__':
    main()