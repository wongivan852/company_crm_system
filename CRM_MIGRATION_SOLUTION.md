# CRM Migration Solution - Complete Fix

## Problem Analysis

Based on the `CRM_MIGRATION_ISSUE_SUMMARY.md`, the main issues are:

1. **Database Migration Failures**: Django migrations failing due to existing tables and constraints
2. **Database State Inconsistency**: Database appears empty but still contains dependent objects
3. **CSV Header Mismatch**: Original CSV headers don't match Django model field names
4. **Connection Issues**: Active database connections preventing clean database reset

## Root Cause

The core issue is that PostgreSQL has dependent objects (foreign keys, indexes, sequences) that prevent clean table dropping, even after database recreation. This happens when:
- Previous migration attempts left orphaned constraints
- Database connections weren't properly terminated
- Schema objects weren't completely cleared

## Complete Solution

### Option 1: Automated Fix (Recommended)

Use the provided troubleshooting script for a complete automated solution:

```bash
# Make script executable
chmod +x migration_troubleshooting.sh

# Run complete fix
sudo ./migration_troubleshooting.sh
```

### Option 2: Manual Step-by-Step Fix

#### Step 1: Complete Database Reset

```bash
# Stop all services using the database
sudo systemctl stop nginx
sudo pkill -f "python.*manage.py"

# Kill all database connections
sudo -u postgres psql -c "
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'crm_db' AND pid <> pg_backend_pid();"

# Complete database cleanup
sudo -u postgres dropdb --if-exists crm_db
sudo -u postgres psql -c "DROP USER IF EXISTS crm_user;"

# Recreate user and database
sudo -u postgres psql -c "CREATE USER crm_user WITH PASSWORD '5514';"
sudo -u postgres psql -c "ALTER USER crm_user CREATEDB;"
sudo -u postgres createdb -O crm_user crm_db
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE crm_db TO crm_user;"
```

#### Step 2: Verify Clean Database

```bash
# Check database is empty
sudo -u postgres psql -d crm_db -c "\dt"
# Should show "No relations found."

# If tables still exist, force clean schema
sudo -u postgres psql -d crm_db -c "
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO crm_user;
GRANT ALL ON SCHEMA public TO public;"
```

#### Step 3: Django Migration Reset

```bash
cd /home/ubuntu/company_crm_system/crm_project

# Clear all migration files
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Create fresh migrations
python manage.py makemigrations
python manage.py migrate
```

#### Step 4: Import YouTube Data

```bash
# Use the fixed CSV with correct headers
python manage.py shell -c "
import csv
from crm.models import Customer

with open('../youtube_creators_import_fixed.csv', 'r') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        youtube_handle = row.get('youtube_handle', '').strip()
        if not youtube_handle:
            continue
            
        if Customer.objects.filter(youtube_handle__iexact=youtube_handle).exists():
            continue
        
        customer = Customer(
            first_name=row.get('first_name', '').strip() or youtube_handle.replace('_', ' ').title(),
            last_name=row.get('last_name', '').strip() or 'Creator',
            email_primary=row.get('primary_email', '').strip() or None,
            youtube_handle=youtube_handle,
            youtube_channel_url=row.get('youtube_channel_url', '').strip(),
            company_primary=row.get('company_primary', '').strip(),
            customer_type=row.get('customer_type', 'youtuber').strip(),
            status=row.get('status', 'prospect').strip(),
            source=row.get('referral_source', 'youtube_import').strip(),
            preferred_communication_method=row.get('preferred_communication_method', 'email').strip(),
            country_region=row.get('country_region', '').strip(),
            position_primary=row.get('position_primary', '').strip(),
        )
        
        customer.save()
        print(f'✓ Imported: @{youtube_handle}')

print(f'Total YouTubers: {Customer.objects.filter(customer_type=\"youtuber\").count()}')
"
```

## CSV Format Fix

The `youtube_creators_import_fixed.csv` has been corrected with proper Django field names:

**Original Headers** → **Fixed Headers**
- `First Name` → `first_name`
- `Last Name` → `last_name`  
- `Primary Email` → `primary_email`
- `Customer Type` → `customer_type`
- `YouTube Handle` → `youtube_handle`
- `YouTube Channel URL` → `youtube_channel_url`
- `Primary Company` → `company_primary`
- `Source` → `referral_source`
- `Preferred Communication Method` → `preferred_communication_method`
- `Country/Region` → `country_region`
- `Primary Position` → `position_primary`

## Verification Steps

After running the solution:

1. **Check Database Status:**
   ```bash
   python manage.py shell -c "from django.db import connection; print(connection.queries)"
   ```

2. **Verify YouTube Import:**
   ```bash
   python manage.py shell -c "from crm.models import Customer; print(f'YouTube creators: {Customer.objects.filter(customer_type=\"youtuber\").count()}')"
   ```

3. **Test Server:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

4. **Access Admin:**
   - URL: `http://your-server-ip:8000/admin/`
   - Login: `admin` / `admin123` (created by script)

## Prevention Measures

To prevent future migration issues:

1. **Always terminate connections before database operations:**
   ```bash
   sudo -u postgres psql -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'crm_db';"
   ```

2. **Use transactions for migrations:**
   ```python
   # In Django settings
   DATABASES = {
       'default': {
           # ... other settings
           'ATOMIC_REQUESTS': True,
       }
   }
   ```

3. **Regular database backups:**
   ```bash
   sudo -u postgres pg_dump crm_db > crm_backup_$(date +%Y%m%d).sql
   ```

## Troubleshooting Commands

If issues persist:

```bash
# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-*-main.log

# Check Django migration status
python manage.py showmigrations

# Force reset specific app migrations
python manage.py migrate crm zero
python manage.py migrate crm

# Check database permissions
sudo -u postgres psql -d crm_db -c "\du"
```

## Expected Results

After successful completion:
- ✅ Clean PostgreSQL database with no orphaned objects
- ✅ All Django migrations applied successfully  
- ✅ 49 YouTube creators imported with correct data structure
- ✅ Django server running without errors
- ✅ Admin interface accessible for data management

This solution addresses all the issues mentioned in the migration summary and provides a robust foundation for the CRM system on your Dell server.