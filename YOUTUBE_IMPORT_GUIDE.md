# YouTube Creators Import Guide

## Overview
This guide explains how to import YouTube creators into the CRM system without affecting existing customer data.

## Files Created

### 1. YouTube Creators CSV
**File:** `youtube_creators_import.csv`
- Contains 49 YouTube creators from your provided list
- Properly formatted for CRM import
- Includes all required fields: YouTube Handle, Channel URL, Customer Type

### 2. Enhanced Import Script
**File:** `crm_project/import_customers.py` (enhanced)
- Added YouTube field mapping support
- Added dedicated `import_youtube_creators()` function
- Safe import with duplicate detection

## Import Process

### Method 1: YouTube-Only Import (Recommended for your case)
```bash
cd /Users/wongivan/ai_tools/business_tools/company_crm_system/crm_project
python import_customers.py youtube
```

### Method 2: Full Import (includes YouTube if CSV exists)
```bash
cd /Users/wongivan/ai_tools/business_tools/company_crm_system/crm_project
python import_customers.py
```

## Import Results

✅ **Successfully Imported:** 49 YouTube creators
- All creators assigned `customer_type='youtuber'`
- YouTube handles cleaned (@ removed)
- Channel URLs auto-generated where missing
- No duplicates or errors

## Sample Imported Data

| Handle | Name | Company | Type |
|--------|------|---------|------|
| @blenderguru | Blender Guru | Blender Guru Studio | youtuber |
| @robbybranham | CG Fast Track | CG Fast Track | youtuber |
| @KevinStratvert | Kevin Stratvert | Kevin Stratvert | youtuber |
| @Brackeys | Brackeys Team | Brackeys | youtuber |
| @cgboost | CG Boost | CG Boost | youtuber |

## Database Verification

Check current YouTube creators:
```bash
python manage.py shell -c "from crm.models import Customer; print(f'YouTube creators: {Customer.objects.filter(customer_type=\"youtuber\").count()}')"
```

## Safety Features

1. **Duplicate Detection**: Checks for existing YouTube handles and emails
2. **No Data Overwrite**: Skips existing customers, doesn't modify current data
3. **Error Handling**: Continues import even if individual records fail
4. **Validation**: Ensures required fields are present

## CSV Format

The CSV uses these column headers:
- `First Name`, `Last Name`
- `YouTube Handle`, `YouTube Channel URL`
- `Customer Type` (set to 'youtuber')
- `Primary Company`, `Status`, `Source`
- `Preferred Communication Method`
- `Country/Region`, `Primary Position`

## Next Steps for Dell Server

To import to your Dell server:

1. **Transfer Files:**
   ```bash
   scp youtube_creators_import.csv user@dell-server:/path/to/crm/
   scp crm_project/import_customers.py user@dell-server:/path/to/crm/crm_project/
   ```

2. **Run Import on Dell Server:**
   ```bash
   ssh user@dell-server
   cd /path/to/crm/crm_project
   python import_customers.py youtube
   ```

3. **Verify Import:**
   ```bash
   python manage.py shell -c "from crm.models import Customer; print(Customer.objects.filter(customer_type='youtuber').count())"
   ```

## Troubleshooting

- **Database Migration Issues**: Run `python manage.py migrate` first
- **Permission Issues**: Ensure Django settings are correct
- **Duplicate Warnings**: Normal - existing customers are safely skipped

## Contact

The import script includes comprehensive error handling and logging for any issues that may arise during the import process.