#!/bin/bash

# Database Backup Script for CRM System
# This script creates automated backups of the PostgreSQL database

set -e  # Exit on any error

# Configuration
BACKUP_DIR="/app/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="${DB_NAME:-crm_db}"
DB_USER="${DB_USER:-crm_user}"
RETENTION_DAYS=${BACKUP_RETENTION_DAYS:-30}

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Backup filename
BACKUP_FILE="$BACKUP_DIR/crm_backup_$DATE.sql.gz"

echo "Starting database backup at $(date)"
echo "Database: $DB_NAME"
echo "User: $DB_USER"
echo "Backup file: $BACKUP_FILE"

# Create the backup
if docker-compose exec -T db pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_FILE"; then
    echo "Backup completed successfully"
    
    # Get file size
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "Backup size: $BACKUP_SIZE"
    
    # Verify backup integrity
    if gzip -t "$BACKUP_FILE"; then
        echo "Backup integrity verified"
    else
        echo "ERROR: Backup integrity check failed"
        exit 1
    fi
    
    # Clean up old backups
    echo "Cleaning up backups older than $RETENTION_DAYS days..."
    find "$BACKUP_DIR" -name "crm_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete
    
    # Count remaining backups
    REMAINING_BACKUPS=$(find "$BACKUP_DIR" -name "crm_backup_*.sql.gz" | wc -l)
    echo "Remaining backups: $REMAINING_BACKUPS"
    
    echo "Database backup completed at $(date)"
    
    # Log to system logger if available
    if command -v logger >/dev/null 2>&1; then
        logger "CRM Database backup completed successfully: $BACKUP_FILE ($BACKUP_SIZE)"
    fi
    
else
    echo "ERROR: Backup failed"
    # Log error to system logger if available
    if command -v logger >/dev/null 2>&1; then
        logger "ERROR: CRM Database backup failed"
    fi
    exit 1
fi