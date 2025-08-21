#!/usr/bin/env python
"""
Database Synchronization Verification Script
Compares data between MacBook (SQLite) and Dell Server (PostgreSQL) environments
"""
import os
import sys
import json
from pathlib import Path

def analyze_macbook_data():
    """Analyze MacBook SQLite database"""
    print("🔍 Analyzing MacBook Environment Data")
    print("=" * 50)
    
    # Look for SQLite database
    sqlite_paths = [
        Path.cwd() / "db.sqlite3",
        Path.cwd().parent / "db.sqlite3",
        Path("~/ai_tools/business_tools/company_crm_system/crm_project/db.sqlite3").expanduser()
    ]
    
    sqlite_db = None
    for path in sqlite_paths:
        if path.exists():
            sqlite_db = path
            print(f"📂 Found SQLite database: {sqlite_db}")
            break
    
    if not sqlite_db:
        print("❌ SQLite database not found in expected locations")
        return None
    
    # Connect to SQLite and analyze
    import sqlite3
    try:
        conn = sqlite3.connect(sqlite_db)
        cursor = conn.cursor()
        
        # Get customer count
        cursor.execute("SELECT COUNT(*) FROM crm_customer")
        total_count = cursor.fetchone()[0]
        print(f"📊 Total customers: {total_count}")
        
        # Get count by customer type
        cursor.execute("""
            SELECT customer_type, COUNT(*) 
            FROM crm_customer 
            GROUP BY customer_type 
            ORDER BY COUNT(*) DESC
        """)
        type_counts = dict(cursor.fetchall())
        print("📊 By customer type:")
        for ctype, count in type_counts.items():
            print(f"  - {ctype}: {count}")
        
        # Get count by source
        cursor.execute("""
            SELECT source, COUNT(*) 
            FROM crm_customer 
            GROUP BY source 
            ORDER BY COUNT(*) DESC 
            LIMIT 10
        """)
        source_counts = dict(cursor.fetchall())
        print("📊 Top sources:")
        for source, count in source_counts.items():
            print(f"  - {source}: {count}")
        
        # Check for YouTube creators
        cursor.execute("SELECT COUNT(*) FROM crm_customer WHERE customer_type = 'youtuber'")
        youtube_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM crm_customer WHERE youtube_handle IS NOT NULL AND youtube_handle != ''")
        youtube_with_handles = cursor.fetchone()[0]
        
        print(f"📊 YouTube creators: {youtube_count} total, {youtube_with_handles} with handles")
        
        # Sample data for verification
        cursor.execute("SELECT id, first_name, last_name, email_primary, customer_type FROM crm_customer LIMIT 10")
        samples = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_count': total_count,
            'type_counts': type_counts,
            'source_counts': source_counts,
            'youtube_count': youtube_count,
            'youtube_with_handles': youtube_with_handles,
            'sample_records': samples[:5]  # First 5 for comparison
        }
        
    except Exception as e:
        print(f"❌ Error analyzing SQLite database: {e}")
        return None

def analyze_postgresql_data():
    """Analyze PostgreSQL database (Docker environment)"""
    print("\n🔍 Analyzing Dell Server Environment Data")
    print("=" * 50)
    
    # Setup Django for PostgreSQL analysis
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
    
    try:
        import django
        django.setup()
        from crm.models import Customer
        from django.db.models import Count
        
        # Get customer count
        total_count = Customer.objects.count()
        print(f"📊 Total customers: {total_count}")
        
        # Get count by customer type
        type_counts = dict(Customer.objects.values('customer_type').annotate(count=Count('customer_type')).values_list('customer_type', 'count'))
        print("📊 By customer type:")
        for ctype, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {ctype}: {count}")
        
        # Get count by source
        source_counts = dict(Customer.objects.values('source').annotate(count=Count('source')).order_by('-count')[:10].values_list('source', 'count'))
        print("📊 Top sources:")
        for source, count in source_counts.items():
            print(f"  - {source}: {count}")
        
        # Check for YouTube creators
        youtube_count = Customer.objects.filter(customer_type='youtuber').count()
        youtube_with_handles = Customer.objects.exclude(youtube_handle__isnull=True).exclude(youtube_handle='').count()
        
        print(f"📊 YouTube creators: {youtube_count} total, {youtube_with_handles} with handles")
        
        # Sample data for verification
        samples = list(Customer.objects.values('id', 'first_name', 'last_name', 'email_primary', 'customer_type')[:5])
        
        return {
            'total_count': total_count,
            'type_counts': type_counts,
            'source_counts': source_counts,
            'youtube_count': youtube_count,
            'youtube_with_handles': youtube_with_handles,
            'sample_records': samples
        }
        
    except Exception as e:
        print(f"❌ Error analyzing PostgreSQL database: {e}")
        import traceback
        traceback.print_exc()
        return None

def compare_environments(macbook_data, postgres_data):
    """Compare data between environments and identify discrepancies"""
    print("\n🔍 ENVIRONMENT COMPARISON ANALYSIS")
    print("=" * 60)
    
    if not macbook_data or not postgres_data:
        print("❌ Cannot compare - missing data from one or both environments")
        return
    
    # Total count comparison
    mb_total = macbook_data['total_count']
    pg_total = postgres_data['total_count']
    difference = abs(mb_total - pg_total)
    
    print(f"📊 TOTAL RECORDS COMPARISON:")
    print(f"  MacBook (SQLite): {mb_total:,} records")
    print(f"  Dell Server (PostgreSQL): {pg_total:,} records")
    print(f"  Difference: {difference:,} records")
    
    if difference > 0:
        missing_env = "Dell Server" if mb_total > pg_total else "MacBook"
        print(f"  ⚠️ {missing_env} is missing {difference:,} records")
    else:
        print("  ✅ Record counts match!")
    
    # Customer type comparison
    print(f"\n📊 CUSTOMER TYPE COMPARISON:")
    all_types = set(macbook_data['type_counts'].keys()) | set(postgres_data['type_counts'].keys())
    
    for ctype in sorted(all_types):
        mb_count = macbook_data['type_counts'].get(ctype, 0)
        pg_count = postgres_data['type_counts'].get(ctype, 0)
        type_diff = abs(mb_count - pg_count)
        
        status = "✅" if type_diff == 0 else f"⚠️ ({type_diff:,} diff)"
        print(f"  {ctype}:")
        print(f"    MacBook: {mb_count:,}, Dell Server: {pg_count:,} {status}")
    
    # Source comparison
    print(f"\n📊 SOURCE COMPARISON (Top 10):")
    all_sources = set(macbook_data['source_counts'].keys()) | set(postgres_data['source_counts'].keys())
    
    for source in sorted(all_sources, key=lambda x: macbook_data['source_counts'].get(x, 0) + postgres_data['source_counts'].get(x, 0), reverse=True)[:10]:
        mb_count = macbook_data['source_counts'].get(source, 0)
        pg_count = postgres_data['source_counts'].get(source, 0)
        source_diff = abs(mb_count - pg_count)
        
        if mb_count > 0 or pg_count > 0:  # Only show non-zero sources
            status = "✅" if source_diff == 0 else f"⚠️ ({source_diff:,} diff)"
            print(f"  {source}:")
            print(f"    MacBook: {mb_count:,}, Dell Server: {pg_count:,} {status}")
    
    # YouTube creators comparison
    print(f"\n📊 YOUTUBE CREATORS COMPARISON:")
    mb_youtube = macbook_data['youtube_count']
    pg_youtube = postgres_data['youtube_count']
    youtube_diff = abs(mb_youtube - pg_youtube)
    
    print(f"  Total YouTube creators:")
    print(f"    MacBook: {mb_youtube:,}, Dell Server: {pg_youtube:,}")
    if youtube_diff > 0:
        print(f"    ⚠️ Difference: {youtube_diff:,} YouTube creators")
    else:
        print(f"    ✅ YouTube creator counts match")
    
    # Recommendations based on analysis
    print(f"\n💡 RECOMMENDATIONS:")
    print("=" * 30)
    
    if difference > 100:
        print("🔴 CRITICAL: Large data discrepancy detected!")
        print("   Recommended actions:")
        print("   1. Run complete data re-import on Dell server")
        print("   2. Verify all CSV dataset files are accessible in Docker")
        print("   3. Check Docker volume mounting configuration")
        print("   4. Review import error logs")
    elif difference > 10:
        print("🟡 MODERATE: Some data discrepancy detected")
        print("   Recommended actions:")
        print("   1. Check for import errors in specific datasets")
        print("   2. Verify duplicate handling logic")
        print("   3. Run incremental import for missing records")
    else:
        print("🟢 GOOD: Data counts are very close or identical")
        print("   Minor differences may be due to:")
        print("   - Recent additions in one environment")
        print("   - Different duplicate handling")
    
    # Specific checks for the 100+ missing records issue
    if mb_total > pg_total and difference >= 100:
        print(f"\n🔍 SPECIFIC ANALYSIS FOR MISSING {difference:,} RECORDS:")
        print("   Most likely causes:")
        print("   1. Docker volume mounting issues preventing dataset access")
        print("   2. Import script failing silently on specific datasets")
        print("   3. PostgreSQL constraint violations not present in SQLite")
        print("   4. Transaction rollbacks due to data integrity issues")
        print("   5. Memory or connection timeout issues during large imports")
        
        print(f"\n🔧 IMMEDIATE FIXES TO TRY:")
        print("   1. Use fixed Docker Compose file (docker-compose-fixed.yml)")
        print("   2. Run robust import script (import_customers_robust.py)")
        print("   3. Use enhanced entrypoint (entrypoint-fixed.sh)")
        print("   4. Check /app/logs/import.log for detailed error information")

def main():
    """Main function to run environment comparison"""
    print("🔍 CRM DATABASE SYNCHRONIZATION VERIFICATION")
    print("=" * 60)
    print("This script compares customer data between MacBook and Dell server environments")
    print("to identify the cause of missing 100+ records.\n")
    
    # Analyze both environments
    macbook_data = analyze_macbook_data()
    postgres_data = analyze_postgresql_data()
    
    # Compare and provide recommendations
    compare_environments(macbook_data, postgres_data)
    
    # Save analysis results
    results = {
        'macbook_environment': macbook_data,
        'postgresql_environment': postgres_data,
        'analysis_timestamp': str(datetime.now())
    }
    
    try:
        from datetime import datetime
        with open('/app/logs/sync_analysis.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Analysis results saved to: /app/logs/sync_analysis.json")
    except:
        print(f"\n💾 Could not save analysis results")

if __name__ == "__main__":
    main()