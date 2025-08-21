#!/bin/bash
# CRM Migration Troubleshooting Script
# Comprehensive solution for Dell server database migration issues

set -e  # Exit on any error

echo "🔧 CRM Migration Troubleshooting Script"
echo "========================================"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DB_NAME="crm_db"
DB_USER="crm_user"
DB_PASSWORD="5514"
DJANGO_DIR="/home/user/krystal-company-apps/company_crm_system/crm_project"

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Step 1: Check PostgreSQL status
check_postgresql() {
    log_info "Checking PostgreSQL service status..."
    if sudo systemctl is-active --quiet postgresql; then
        log_success "PostgreSQL is running"
    else
        log_error "PostgreSQL is not running. Starting..."
        sudo systemctl start postgresql
        sudo systemctl enable postgresql
    fi
}

# Step 2: Verify database connections
check_connections() {
    log_info "Checking active database connections..."
    
    # Kill all connections to the database
    sudo -u postgres psql -c "
    SELECT pg_terminate_backend(pid)
    FROM pg_stat_activity
    WHERE datname = '$DB_NAME' AND pid <> pg_backend_pid();"
    
    log_success "Terminated all connections to $DB_NAME"
}

# Step 3: Completely reset database
reset_database() {
    log_info "Completely resetting database $DB_NAME..."
    
    # Step 3a: Kill connections first
    check_connections
    
    # Step 3b: Drop database if exists
    log_info "Dropping database $DB_NAME..."
    sudo -u postgres dropdb --if-exists $DB_NAME
    
    # Step 3c: Drop and recreate user to reset permissions
    log_info "Resetting database user $DB_USER..."
    sudo -u postgres psql -c "DROP USER IF EXISTS $DB_USER;"
    sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
    sudo -u postgres psql -c "ALTER USER $DB_USER CREATEDB;"
    
    # Step 3d: Create fresh database
    log_info "Creating fresh database $DB_NAME..."
    sudo -u postgres createdb -O $DB_USER $DB_NAME
    
    # Step 3e: Grant all privileges
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
    
    log_success "Database $DB_NAME completely reset"
}

# Step 4: Verify database is empty
verify_empty_database() {
    log_info "Verifying database is empty..."
    
    TABLE_COUNT=$(sudo -u postgres psql -d $DB_NAME -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
    
    if [ "$TABLE_COUNT" -eq 0 ]; then
        log_success "Database is empty - ready for migrations"
    else
        log_error "Database still contains $TABLE_COUNT tables"
        
        # Show existing tables
        log_info "Existing tables:"
        sudo -u postgres psql -d $DB_NAME -c "\dt"
        
        # Force cleanup
        log_warning "Force cleaning remaining objects..."
        sudo -u postgres psql -d $DB_NAME -c "
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
        GRANT ALL ON SCHEMA public TO $DB_USER;
        GRANT ALL ON SCHEMA public TO public;"
        
        log_success "Force cleanup completed"
    fi
}

# Step 5: Update Django settings and environment
update_django_config() {
    log_info "Updating Django configuration..."
    
    # Update .env file
    ENV_FILE="/home/user/krystal-company-apps/company_crm_system/.env"
    
    if [ -f "$ENV_FILE" ]; then
        log_info "Updating $ENV_FILE..."
        sed -i "s/^DB_PASSWORD=.*/DB_PASSWORD=$DB_PASSWORD/" "$ENV_FILE"
        sed -i "s/^DB_NAME=.*/DB_NAME=$DB_NAME/" "$ENV_FILE"
        sed -i "s/^DB_USER=.*/DB_USER=$DB_USER/" "$ENV_FILE"
    else
        log_warning ".env file not found, creating one..."
        cat > "$ENV_FILE" << EOF
DEBUG=False
SECRET_KEY=your-secret-key-here
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1,your-server-ip
EOF
    fi
    
    log_success "Django configuration updated"
}

# Step 6: Run Django migrations
run_migrations() {
    log_info "Running Django migrations..."
    
    cd "$DJANGO_DIR" || exit 1
    # Activate virtual environment

# Step 7: Create superuser
create_superuser() {
    log_info "Creating Django superuser..."
    
    cd "$DJANGO_DIR" || exit 1
    # Activate virtual environment
    PYTHON_BIN="/home/user/krystal-company-apps/company_crm_system/.venv/bin/python"
    # Create superuser non-interactively
    "$PYTHON_BIN" manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"
    
    log_success "Superuser setup completed"
}

# Step 8: Test database connection
test_connection() {
    log_info "Testing database connection..."
    
    cd "$DJANGO_DIR" || exit 1
    # Activate virtual environment
    PYTHON_BIN="/home/user/krystal-company-apps/company_crm_system/.venv/bin/python"
    "$PYTHON_BIN" manage.py shell -c "
from django.db import connection
cursor = connection.cursor()
cursor.execute('SELECT version()')
version = cursor.fetchone()[0]
print(f'Database connection successful: {version}')
"
    
    log_success "Database connection test passed"
}

# Step 9: Import YouTube creators
import_youtube_data() {
    log_info "Importing YouTube creators data..."
    
    PYTHON_BIN="/home/user/krystal-company-apps/company_crm_system/.venv/bin/python"
    # Use the fixed CSV with correct headers
    CSV_FILE="../youtube_creators_import_fixed.csv"
        if [ -f "$CSV_FILE" ]; then
            log_info "Found fixed CSV file, importing..."
            "$PYTHON_BIN" manage.py import_youtube_creators --file="$CSV_FILE"
            log_success "YouTube data import completed"
        else
            log_warning "Fixed CSV file not found, skipping YouTube import"
        fi
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
            imported += 1
            print(f'✓ Imported: @{youtube_handle}')
            
        except Exception as e:
            errors += 1
            print(f'✗ Error: {e}')

print(f'Import complete: {imported} imported, {errors} errors')
print(f'Total YouTubers: {Customer.objects.filter(customer_type=\"youtuber\").count()}')
"
        
        log_success "YouTube data import completed"
    else
        log_warning "Fixed CSV file not found, skipping YouTube import"
    fi
}

# Main execution
main() {
    log_info "Starting CRM migration troubleshooting process..."
    
    # Execute all steps
    check_postgresql
    check_connections
    reset_database
    verify_empty_database
    update_django_config
    run_migrations
    create_superuser
    test_connection
    import_youtube_data
    
    log_success "🎉 CRM migration troubleshooting completed successfully!"
    log_info "Next steps:"
    echo "  1. Start Django server: cd $DJANGO_DIR && python manage.py runserver 0.0.0.0:8000"
    echo "  2. Access admin: http://your-server-ip:8000/admin/"
    echo "  3. Login with: admin/admin123"
    echo "  4. Verify YouTube creators in customer list"
}

# Handle script arguments
case "${1:-}" in
    "reset-db")
        check_postgresql
        check_connections
        reset_database
        verify_empty_database
        ;;
    "migrate")
        update_django_config
        run_migrations
        ;;
    "import")
        import_youtube_data
        ;;
    "test")
        test_connection
        ;;
    *)
        main
        ;;
esac