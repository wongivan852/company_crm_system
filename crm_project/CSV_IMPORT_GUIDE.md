# CSV Customer Import Guide

## Overview
The CRM system provides a robust CSV import feature that can handle various CSV formats with flexible field mapping and comprehensive validation.

## Supported Field Variations

### Required Fields (Must be present)
- **First Name**: `first_name`, `firstname`, `first`, `given_name`, `fname`
- **Last Name**: `last_name`, `lastname`, `last`, `surname`, `family_name`, `lname`
- **Primary Email**: `email`, `email_primary`, `primary_email`, `email_address`, `email1`

### Optional Name Fields
- **Middle Name**: `middle_name`, `middlename`, `middle`, `middle_initial`, `mi`
- **Preferred Name**: `preferred_name`, `nickname`, `display_name`, `known_as`
- **Title**: `title`, `salutation`, `prefix`, `honorific` (Mr., Mrs., Dr., etc.)
- **Suffix**: `suffix`, `name_suffix`, `jr_sr`, `generation` (Jr., Sr., III, etc.)

### Contact Information
- **Primary Email**: `email`, `email_primary`, `primary_email`, `email_address`, `emails`
  - **Multiple Emails Supported**: If a single field contains multiple emails separated by commas, semicolons, pipes, or "and"/"&", the system will automatically split them into primary and secondary emails
- **Secondary Email**: `email_secondary`, `secondary_email`, `email2`, `personal_email`
- **Primary Phone**: `phone`, `phone_number`, `phone_primary`, `mobile`, `cell`
- **Secondary Phone**: `phone_secondary`, `home_phone`, `work_phone`, `office_phone`

### Professional Information
- **Company**: `company`, `company_name`, `organization`, `employer`, `workplace`
- **Position**: `position`, `job_title`, `role`, `designation`, `current_position`

### Geographic Information
- **Country**: `country`, `country_region`, `nationality`, `region`

### Customer Classification
- **Customer Type**: `customer_type`, `type`, `category`, `classification`
  - Accepted values: `individual`, `corporate`, `student`, `instructor`
  - Also accepts variations like: `personal`, `company`, `business`, `learner`, `teacher`

## CSV Format Requirements

### File Format
- **Encoding**: UTF-8 (preferred) or Latin-1
- **File Extension**: `.csv`
- **Max File Size**: 10MB
- **Delimiters**: Comma (`,`), semicolon (`;`), tab (`\t`), or pipe (`|`)

### Header Row
- First row must contain column headers
- Headers are case-insensitive
- Spaces and underscores are interchangeable

### Data Formatting

#### Names
- Automatically converts ALL CAPS to Title Case
- Handles extra whitespace
- If only full name is provided, automatically splits into first/middle/last

#### Emails
- Automatically converts to lowercase
- Validates email format
- Checks for duplicates

#### Phone Numbers
- Removes formatting characters
- Preserves international codes
- Auto-assigns country codes based on country field

#### Customer Types
- Automatically normalizes variations
- Defaults to "individual" if not specified

## Sample CSV Formats

### Basic Format
```csv
first_name,last_name,email,phone,company,position
John,Smith,john.smith@email.com,+1-555-0123,ABC Corp,Manager
Jane,Doe,jane.doe@email.com,+1-555-0124,XYZ Inc,Developer
```

### Extended Format
```csv
title,first_name,middle_name,last_name,suffix,email_primary,email_secondary,phone_primary,company_primary,position_primary,customer_type,country
Dr.,John,Michael,Smith,Jr.,john.smith@email.com,j.smith@personal.com,+1-555-0123,ABC Corp,Senior Manager,corporate,US
Ms.,Jane,Anne,Doe,,jane.doe@email.com,,+1-555-0124,XYZ Inc,Software Developer,individual,CA
```

### Alternative Header Variations
```csv
firstname,lastname,email_address,mobile_number,organization,job_title
John,Smith,john.smith@email.com,555-0123,ABC Corp,Manager
Jane,Doe,jane.doe@email.com,555-0124,XYZ Inc,Developer
```

### Multiple Email Addresses
```csv
first_name,last_name,email,phone,company
John,Smith,"john.work@company.com, john.personal@gmail.com",555-0123,ABC Corp
Jane,Doe,"jane@work.com; jane.personal@email.com",555-0124,XYZ Inc
Bob,Wilson,"bob@company.com | bob.wilson@personal.com",555-0125,Tech Startup
Alice,Brown,"alice@work.com & alice.brown@home.com",555-0126,Consulting
```

### Full Name Format (Auto-split)
```csv
full_name,email,phone,company
"Dr. John Michael Smith Jr.",john.smith@email.com,+1-555-0123,ABC Corp
"Jane Anne Doe",jane.doe@email.com,+1-555-0124,XYZ Inc
```

## Common Import Challenges & Solutions

### 1. Missing Mandatory Fields
**Problem**: CSV missing required fields (first_name, last_name, email_primary)
**Solution**: 
- System will identify missing fields during preview
- Use field mapping to match alternative column names
- Ensure CSV has columns for all required data

### 2. Name Field Arrangement
**Problem**: Names scattered across different columns or formats
**Solutions**:
- Use individual columns: `first_name`, `middle_name`, `last_name`
- Use full name column: System auto-splits "John Michael Smith"
- Mix and match: Some individual fields + full name fallback

### 3. Duplicate Emails
**Problem**: CSV contains duplicate email addresses
**Solution**: System skips duplicates and shows warnings

### 4. Invalid Data Formats
**Problem**: Invalid emails, malformed phone numbers
**Solution**: System validates and reports errors per row

### 5. Encoding Issues
**Problem**: Special characters not displaying correctly
**Solution**: Save CSV as UTF-8 or use Latin-1 encoding

## Import Process

### Step 1: Upload & Preview
- Upload CSV file
- System auto-detects delimiter and field mappings
- Preview shows detected mappings and sample data

### Step 2: Review Mappings
- Verify automatic field mappings
- Check for missing mandatory fields
- Review unmapped columns (will be ignored)

### Step 3: Import
- System validates all data
- Creates customers in bulk
- Provides detailed success/error report

### Step 4: Review Results
- Shows import statistics
- Lists any warnings or skipped records
- Provides link to view imported customers

## Error Handling

### Row-Level Errors
- Invalid email formats
- Missing mandatory data
- Data validation failures

### File-Level Errors
- Unsupported encoding
- Missing headers
- File size too large

### Duplicate Handling
- Existing customers (by email) are skipped
- Warnings provided for review

## Best Practices

1. **Test with Small Files**: Start with 10-20 records to verify mapping
2. **Clean Data First**: Remove duplicates and validate emails beforehand
3. **Use Standard Headers**: Follow common naming conventions
4. **Check Encoding**: Ensure proper UTF-8 encoding for special characters
5. **Backup Data**: Keep original CSV as backup
6. **Review Warnings**: Check all warnings after import

## API Endpoints

### Preview Import
```
POST /api/customers/preview_csv_import/
Content-Type: multipart/form-data
Body: csv_file (file)
```

### Import CSV
```
POST /api/customers/import_csv/
Content-Type: multipart/form-data
Body: 
  - csv_file (file)
  - field_mapping (JSON, optional)
```

## Troubleshooting

### Common Issues
1. **"No headers found"**: Ensure first row contains column names
2. **"Invalid email format"**: Check email addresses for typos
3. **"Missing mandatory fields"**: Verify first_name, last_name, email columns exist
4. **"Encoding error"**: Save CSV as UTF-8 or try Latin-1

### Support
- Check import logs for detailed error messages
- Use preview function to test field mappings
- Contact system administrator for complex data issues

## Example Import Workflow

1. Export sample customer to understand field structure
2. Prepare CSV with proper headers and clean data
3. Use preview function to verify mappings
4. Adjust field mappings if needed
5. Run import and review results
6. Check customer list for imported records