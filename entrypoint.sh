#!/bin/sh

# entrypoint.sh - Docker entrypoint for CRM system

set -e

echo "Starting CRM System initialization..."

# Change to project directory
cd /app/crm_project

# Wait for database to be ready
echo "Waiting for database to be ready..."
while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 2
done

echo "Database is ready!"

# Create necessary directories
mkdir -p /app/logs /app/static /app/media /app/data/datasets

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Load initial data if datasets exist and database is empty
if [ -f "/app/data/datasets/complete_customer_dataset_20250820_035231.csv" ]; then
    echo "Checking if initial data needs to be loaded..."
    # Check if Customer table has data
    CUSTOMER_COUNT=$(python manage.py shell -c "from crm.models import Customer; print(Customer.objects.count())" 2>/dev/null || echo "0")
    if [ "$CUSTOMER_COUNT" = "0" ]; then
        echo "Loading initial customer data..."
        python import_customers.py /app/data/datasets/complete_customer_dataset_20250820_035231.csv || echo "Warning: Could not import customer data"
    else
        echo "Customer data already exists, skipping import."
    fi
fi

# Create superuser if it doesn't exist
echo "Creating superuser if needed..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@crm.local', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
" 2>/dev/null || echo "Warning: Could not create superuser"

echo "Initialization complete! Starting server on port ${PORT:-8083}..."

# Execute the passed command (usually gunicorn)
exec "$@"