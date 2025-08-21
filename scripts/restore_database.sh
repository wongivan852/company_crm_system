#!/bin/bash

# Database Restore Script for CRM System
# This script restores a PostgreSQL database from backup

set -e  # Exit on any error

# Configuration
BACKUP_DIR="/app/backups"
DB_NAME="${DB_NAME:-crm_db}"
DB_USER="${DB_USER:-crm_user}"

# Function to show usage
show_usage() {
    echo "Usage: $0 <backup_file>"
    echo "Example: $0 crm_backup_20241221_143022.sql.gz"
    echo ""
    echo "Available backups:"
    find "$BACKUP_DIR" -name "crm_backup_*.sql.gz" -printf "%f %TY-%Tm-%Td %TH:%TM\n" | sort -r | head -10
}

# Check if backup file is provided
if [ $# -eq 0 ]; then
    show_usage
    exit 1
fi

BACKUP_FILE="$1"

# Check if backup file exists (try both absolute and relative paths)
if [ -f "$BACKUP_FILE" ]; then
    FULL_BACKUP_PATH="$BACKUP_FILE"
elif [ -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
    FULL_BACKUP_PATH="$BACKUP_DIR/$BACKUP_FILE"
else
    echo "ERROR: Backup file not found: $BACKUP_FILE"
    show_usage
    exit 1
fi

echo "WARNING: This will replace the current database!"
echo "Database: $DB_NAME"
echo "Backup file: $FULL_BACKUP_PATH"
echo ""
echo "Are you sure you want to continue? (type 'yes' to confirm)"
read -r confirmation

if [ "$confirmation" != "yes" ]; then
    echo "Restore cancelled"
    exit 0
fi

echo "Starting database restore at $(date)"

# Verify backup integrity before restore
echo "Verifying backup integrity..."
if ! gzip -t "$FULL_BACKUP_PATH"; then
    echo "ERROR: Backup file is corrupted or invalid"
    exit 1
fi
echo "Backup integrity verified"

# Create a safety backup before restore
SAFETY_BACKUP="$BACKUP_DIR/pre_restore_backup_$(date +%Y%m%d_%H%M%S).sql.gz"
echo "Creating safety backup: $SAFETY_BACKUP"
docker-compose exec -T db pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$SAFETY_BACKUP"

# Drop and recreate database
echo "Dropping existing database..."
docker-compose exec -T db psql -U "$DB_USER" -c "DROP DATABASE IF EXISTS ${DB_NAME};"
echo "Creating new database..."
docker-compose exec -T db psql -U "$DB_USER" -c "CREATE DATABASE ${DB_NAME};"

# Restore from backup
echo "Restoring database from backup..."
if gunzip -c "$FULL_BACKUP_PATH" | docker-compose exec -T db psql -U "$DB_USER" -d "$DB_NAME"; then
    echo "Database restore completed successfully at $(date)"
    
    # Log to system logger if available
    if command -v logger >/dev/null 2>&1; then
        logger "CRM Database restore completed successfully from: $FULL_BACKUP_PATH"
    fi
    
    echo ""
    echo "IMPORTANT: Please restart the application services to ensure proper database connection:"
    echo "docker-compose restart web celery celery-beat"
    
else
    echo "ERROR: Database restore failed"
    echo "Attempting to restore from safety backup..."
    
    if gunzip -c "$SAFETY_BACKUP" | docker-compose exec -T db psql -U "$DB_USER" -d "$DB_NAME"; then
        echo "Successfully restored from safety backup"
    else
        echo "CRITICAL ERROR: Failed to restore from safety backup!"
        echo "Database may be in an inconsistent state"
    fi
    
    # Log error to system logger if available
    if command -v logger >/dev/null 2>&1; then
        logger "ERROR: CRM Database restore failed from: $FULL_BACKUP_PATH"
    fi
    exit 1
fi