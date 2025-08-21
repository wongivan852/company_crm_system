#!/bin/sh

# entrypoint-fixed.sh - Enhanced Docker entrypoint for CRM system
# Fixes database synchronization issues between environments

set -e

echo "🚀 Starting CRM System initialization..."

# Change to project directory
cd /app/crm_project

# Wait for database to be ready with timeout
echo "⏳ Waiting for database to be ready..."
TIMEOUT=60
TIMER=0
while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
    echo "⏳ Waiting for PostgreSQL to be ready... ($TIMER/$TIMEOUT)"
    sleep 2
    TIMER=$((TIMER + 2))
    if [ $TIMER -ge $TIMEOUT ]; then
        echo "❌ Database connection timeout after ${TIMEOUT}s"
        exit 1
    fi
done

echo "✅ Database is ready!"

# Create necessary directories
mkdir -p /app/logs /app/static /app/media /app/data/datasets

# Verify database connection
echo "🔍 Verifying database connection..."
python manage.py shell -c "
from django.db import connection
try:
    cursor = connection.cursor()
    cursor.execute('SELECT version()')
    version = cursor.fetchone()[0]
    print(f'✅ Database connection successful: PostgreSQL')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    exit(1)
" || exit 1

# Run database migrations
echo "📦 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# Check current database state
echo "🔍 Checking current database state..."
CUSTOMER_COUNT=$(python manage.py shell -c "
from crm.models import Customer
count = Customer.objects.count()
print(count)
" 2>/dev/null || echo "0")

echo "📊 Current customer count: $CUSTOMER_COUNT"

# Import data based on current state and available datasets
DATASETS_DIR="/app/data/datasets"
if [ -d "$DATASETS_DIR" ]; then
    DATASET_COUNT=$(find "$DATASETS_DIR" -name "*.csv" | wc -l)
    echo "📂 Found $DATASET_COUNT dataset files in $DATASETS_DIR"
    
    # List available datasets
    echo "📋 Available datasets:"
    for file in "$DATASETS_DIR"/*.csv; do
        if [ -f "$file" ]; then
            filename=$(basename "$file")
            size=$(du -h "$file" | cut -f1)
            echo "  - $filename ($size)"
        fi
    done
    
    # Robust import strategy
    if [ "$CUSTOMER_COUNT" -lt "100" ]; then
        echo "🔄 Low customer count detected. Running robust import..."
        
        # Use the robust import script
        if [ -f "import_customers_robust.py" ]; then
            echo "🚀 Running robust import script..."
            python import_customers_robust.py || {
                echo "⚠️ Robust import failed, trying fallback..."
                
                # Fallback to original import
                if [ -f "/app/data/datasets/complete_customer_dataset_20250820_035231.csv" ]; then
                    echo "📥 Running fallback import..."
                    python import_customers.py "/app/data/datasets/complete_customer_dataset_20250820_035231.csv"
                fi
            }
        else
            echo "⚠️ Robust import script not found, using fallback..."
            if [ -f "/app/data/datasets/complete_customer_dataset_20250820_035231.csv" ]; then
                python import_customers.py "/app/data/datasets/complete_customer_dataset_20250820_035231.csv"
            fi
        fi
        
        # Verify import results
        NEW_COUNT=$(python manage.py shell -c "
from crm.models import Customer
count = Customer.objects.count()
print(count)
" 2>/dev/null || echo "0")
        
        echo "📊 Customer count after import: $NEW_COUNT"
        
        if [ "$NEW_COUNT" -lt "900" ]; then
            echo "⚠️ WARNING: Customer count ($NEW_COUNT) is lower than expected (900+)"
            echo "📋 This may indicate missing data or import issues"
            
            # Try importing additional datasets
            for dataset in "$DATASETS_DIR"/*.csv; do
                if [ -f "$dataset" ] && [ "$(basename "$dataset")" != "complete_customer_dataset_20250820_035231.csv" ]; then
                    echo "📥 Attempting to import additional dataset: $(basename "$dataset")"
                    python import_customers.py "$dataset" || echo "⚠️ Failed to import $(basename "$dataset")"
                fi
            done
        fi
        
    else
        echo "✅ Sufficient customer data exists ($CUSTOMER_COUNT records)"
        
        # Verify data integrity
        python manage.py shell -c "
from crm.models import Customer
from django.db.models import Count

# Check for missing critical data
total = Customer.objects.count()
print(f'📊 Total customers: {total}')

# Count by type
types = Customer.objects.values('customer_type').annotate(count=Count('customer_type')).order_by('-count')
print('📊 By customer type:')
for item in types:
    print(f'  - {item[\"customer_type\"]}: {item[\"count\"]}')

# Check YouTube creators
youtube_count = Customer.objects.filter(customer_type='youtuber').count()
print(f'📊 YouTube creators: {youtube_count}')

if total < 1000:
    print(f'⚠️ WARNING: Customer count ({total}) below expected threshold (1000+)')
else:
    print('✅ Customer count within expected range')
"
    fi
else
    echo "⚠️ Datasets directory not found: $DATASETS_DIR"
fi

# Create superuser if it doesn't exist
echo "👤 Setting up superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@crm.local', 'admin123')
    print('✅ Superuser created: admin/admin123')
else:
    print('✅ Superuser already exists')
" 2>/dev/null || echo "⚠️ Warning: Could not create superuser"

# Final database verification
echo "🔍 Final database verification..."
FINAL_COUNT=$(python manage.py shell -c "
from crm.models import Customer
from django.db import connection

# Test connection
cursor = connection.cursor()
cursor.execute('SELECT COUNT(*) FROM crm_customer')
db_count = cursor.fetchone()[0]

# Django ORM count
orm_count = Customer.objects.count()

print(f'Database count: {db_count}')
print(f'ORM count: {orm_count}')

if db_count == orm_count:
    print('✅ Database consistency verified')
else:
    print('⚠️ Database consistency issue detected')

print(orm_count)
" 2>/dev/null || echo "0")

echo "📊 Final customer count: $FINAL_COUNT"

# Log completion
echo "✅ Initialization complete!"
echo "🔗 Server starting on port ${PORT:-8083}..."
echo "📋 Summary:"
echo "  - Database: PostgreSQL connected"
echo "  - Customers: $FINAL_COUNT records"
echo "  - Admin: admin/admin123"
echo "  - Logs: /app/logs/"

# Execute the passed command (usually gunicorn)
exec "$@"