#!/usr/bin/env python
"""
Robust Customer Import Script - Handles Missing Records Issue
Designed to ensure complete data synchronization between environments
"""
import os
import sys
import django
import csv
import logging
from pathlib import Path
from django.db import transaction, connection
from django.db.utils import IntegrityError

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
django.setup()

from crm.models import Customer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/import.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class RobustCustomerImporter:
    """Robust customer import with comprehensive error handling and verification"""
    
    def __init__(self):
        self.stats = {
            'total_processed': 0,
            'successful_imports': 0,
            'duplicates_skipped': 0,
            'errors': 0,
            'warnings': 0
        }
        self.errors = []
        self.warnings = []

    def verify_database_connection(self):
        """Verify database connection is working"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result[0] == 1:
                    logger.info("✅ Database connection verified")
                    return True
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            return False
        return False

    def get_dataset_files(self):
        """Get all available dataset files with validation"""
        datasets_dir = Path('/app/data/datasets')
        if not datasets_dir.exists():
            logger.error(f"❌ Datasets directory not found: {datasets_dir}")
            return []
        
        csv_files = []
        for pattern in ['*.csv']:
            csv_files.extend(datasets_dir.glob(pattern))
        
        logger.info(f"📊 Found {len(csv_files)} dataset files")
        for csv_file in csv_files:
            size_mb = csv_file.stat().st_size / (1024 * 1024)
            logger.info(f"  - {csv_file.name} ({size_mb:.1f} MB)")
        
        return csv_files

    def validate_csv_structure(self, csv_file):
        """Validate CSV file structure and count rows"""
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)
                row_count = sum(1 for _ in reader)
                
                logger.info(f"📋 {csv_file.name}: {len(headers)} columns, {row_count} data rows")
                logger.info(f"   Headers: {', '.join(headers[:10])}{'...' if len(headers) > 10 else ''}")
                
                return True, row_count, headers
        except Exception as e:
            logger.error(f"❌ Failed to validate {csv_file.name}: {e}")
            return False, 0, []

    def import_complete_dataset(self, csv_file):
        """Import the complete customer dataset with transaction safety"""
        logger.info(f"📥 Starting import: {csv_file.name}")
        
        valid, expected_rows, headers = self.validate_csv_structure(csv_file)
        if not valid:
            return False
        
        imported = 0
        errors = 0
        duplicates = 0
        
        # Use database transaction for consistency
        try:
            with transaction.atomic():
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    
                    for row_num, row in enumerate(reader, 1):
                        try:
                            # Extract required fields
                            email = row.get('email_primary', '').strip() or None
                            first_name = row.get('first_name', '').strip()
                            last_name = row.get('last_name', '').strip()
                            youtube_handle = row.get('youtube_handle', '').strip()
                            
                            # Skip empty rows
                            if not any([email, first_name, last_name, youtube_handle]):
                                continue
                            
                            # Check for existing customers
                            existing_query = Customer.objects.none()
                            
                            if email:
                                existing_query = existing_query | Customer.objects.filter(email_primary=email)
                            if youtube_handle:
                                existing_query = existing_query | Customer.objects.filter(youtube_handle__iexact=youtube_handle)
                            
                            if existing_query.exists():
                                duplicates += 1
                                logger.debug(f"Duplicate found at row {row_num}: {email or youtube_handle}")
                                continue
                            
                            # Create customer record
                            customer_data = {
                                'first_name': first_name or 'Unknown',
                                'last_name': last_name or 'Customer',
                                'email_primary': email,
                                'customer_type': row.get('customer_type', 'individual').strip(),
                                'status': row.get('status', 'prospect').strip(),
                                'company_primary': row.get('company_primary', '').strip(),
                                'phone_primary': row.get('phone_primary', '').strip(),
                                'country_region': row.get('country_region', '').strip(),
                                'source': row.get('source', 'csv_import').strip(),
                                'youtube_handle': youtube_handle or None,
                                'youtube_channel_url': row.get('youtube_channel_url', '').strip(),
                                'linkedin_profile': row.get('linkedin_profile', '').strip(),
                                'twitter_handle': row.get('twitter_handle', '').strip(),
                                'instagram_handle': row.get('instagram_handle', '').strip(),
                                'preferred_communication_method': row.get('preferred_communication_method', 'email').strip(),
                                'marketing_consent': row.get('marketing_consent', '').strip().lower() in ['true', '1', 'yes'],
                            }
                            
                            # Remove empty string values (keep None for optional fields)
                            customer_data = {k: v for k, v in customer_data.items() if v not in ['', None] or k in ['email_primary', 'youtube_handle']}
                            
                            customer = Customer(**customer_data)
                            customer.full_clean()  # Validate before saving
                            customer.save()
                            
                            imported += 1
                            
                            if imported % 100 == 0:
                                logger.info(f"✅ Progress: {imported}/{expected_rows} imported")
                        
                        except IntegrityError as e:
                            duplicates += 1
                            logger.debug(f"Integrity error at row {row_num}: {e}")
                        
                        except Exception as e:
                            errors += 1
                            error_msg = f"Row {row_num}: {str(e)}"
                            self.errors.append(error_msg)
                            logger.error(f"❌ {error_msg}")
                            
                            # Stop if too many errors
                            if errors > 50:
                                logger.error("❌ Too many errors, stopping import")
                                break
                
                # Final verification
                actual_imported = Customer.objects.count()
                logger.info(f"🔍 Verification: {actual_imported} total customers in database")
                
                # Update stats
                self.stats.update({
                    'total_processed': row_num,
                    'successful_imports': imported,
                    'duplicates_skipped': duplicates,
                    'errors': errors
                })
                
                return True
                
        except Exception as e:
            logger.error(f"❌ Transaction failed: {e}")
            return False

    def verify_import_completeness(self):
        """Verify that all expected records are present"""
        logger.info("🔍 Verifying import completeness...")
        
        # Count by customer type
        type_counts = {}
        for customer_type, _ in Customer.CUSTOMER_TYPES:
            count = Customer.objects.filter(customer_type=customer_type).count()
            if count > 0:
                type_counts[customer_type] = count
        
        logger.info("📊 Customer counts by type:")
        for customer_type, count in type_counts.items():
            logger.info(f"  - {customer_type}: {count}")
        
        # Count by source
        source_counts = Customer.objects.values('source').annotate(count=Count('source')).order_by('-count')
        logger.info("📊 Customer counts by source:")
        for item in source_counts[:10]:  # Top 10 sources
            logger.info(f"  - {item['source']}: {item['count']}")
        
        # Check for missing YouTube handles
        youtube_customers = Customer.objects.filter(customer_type='youtuber')
        youtube_with_handles = youtube_customers.exclude(youtube_handle__isnull=True).exclude(youtube_handle='')
        youtube_missing_handles = youtube_customers.filter(youtube_handle__isnull=True) | youtube_customers.filter(youtube_handle='')
        
        logger.info(f"📊 YouTube creators: {youtube_customers.count()} total")
        logger.info(f"  - With handles: {youtube_with_handles.count()}")
        logger.info(f"  - Missing handles: {youtube_missing_handles.count()}")
        
        return Customer.objects.count()

    def run_complete_import(self):
        """Run complete import process with verification"""
        logger.info("🚀 Starting robust customer data import")
        logger.info("=" * 60)
        
        # Step 1: Verify database connection
        if not self.verify_database_connection():
            logger.error("❌ Cannot proceed without database connection")
            return False
        
        # Step 2: Get dataset files
        dataset_files = self.get_dataset_files()
        if not dataset_files:
            logger.error("❌ No dataset files found")
            return False
        
        # Step 3: Import each dataset
        total_success = True
        for csv_file in dataset_files:
            logger.info(f"\n📂 Processing: {csv_file.name}")
            success = self.import_complete_dataset(csv_file)
            if not success:
                total_success = False
                logger.error(f"❌ Failed to import {csv_file.name}")
            else:
                logger.info(f"✅ Successfully processed {csv_file.name}")
        
        # Step 4: Final verification
        total_customers = self.verify_import_completeness()
        
        # Step 5: Summary report
        logger.info("\n" + "=" * 60)
        logger.info("📋 IMPORT SUMMARY REPORT")
        logger.info("=" * 60)
        logger.info(f"✅ Total customers in database: {total_customers}")
        logger.info(f"📥 Records processed: {self.stats['total_processed']}")
        logger.info(f"🎯 Successfully imported: {self.stats['successful_imports']}")
        logger.info(f"🔄 Duplicates skipped: {self.stats['duplicates_skipped']}")
        logger.info(f"❌ Errors encountered: {self.stats['errors']}")
        
        if self.errors:
            logger.info(f"\n⚠️ Error details ({len(self.errors)} total):")
            for error in self.errors[:10]:  # Show first 10 errors
                logger.info(f"  - {error}")
            if len(self.errors) > 10:
                logger.info(f"  ... and {len(self.errors) - 10} more errors")
        
        logger.info("=" * 60)
        
        # Check if we have the expected number of records
        if total_customers < 1000:
            logger.warning(f"⚠️ Expected 1000+ customers but found {total_customers}")
            logger.warning("This may indicate missing data or import issues")
        
        return total_success

if __name__ == "__main__":
    from django.db.models import Count
    
    importer = RobustCustomerImporter()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "verify":
            # Just run verification
            importer.verify_import_completeness()
        elif sys.argv[1] == "count":
            # Just show current count
            count = Customer.objects.count()
            print(f"Current customer count: {count}")
        else:
            # Run import for specific file
            csv_file = Path(sys.argv[1])
            if csv_file.exists():
                importer.import_complete_dataset(csv_file)
            else:
                print(f"File not found: {csv_file}")
    else:
        # Run complete import
        success = importer.run_complete_import()
        sys.exit(0 if success else 1)