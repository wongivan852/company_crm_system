# UAT Testing Instructions for Enhanced CRM System

## Quick Start Guide

### 1. Access the Application
- **Web Interface**: http://127.0.0.1:8001/
- **Admin Interface**: http://127.0.0.1:8001/admin/
- **API Explorer**: http://127.0.0.1:8001/api/v1/

### 2. Test Customer Data Entry

#### Enhanced Customer Fields Available:
- **Basic Info**: First Name, Last Name, Gender, Date of Birth
- **Contact Info**: 
  - Primary Email, Secondary Email
  - Primary Phone, Secondary Phone
  - WhatsApp Number, Fax
- **Address Info**:
  - Primary Address (Line 1, Line 2, City, State, Postal Code)
  - Secondary Address (Line 1, Line 2, City, State, Postal Code)
  - Country, Region
- **Professional Info**: 
  - Company, Primary Position, Secondary Position
  - Company Website
- **Social Media**: 
  - LinkedIn, Facebook, Twitter, Instagram, WeChat ID
- **CRM Fields**: Customer Type, Status, Preferred Communication, Notes

#### To Add a New Customer:
1. Go to http://127.0.0.1:8001/customers/create/
2. Fill in the enhanced form with all available fields
3. Test different communication preferences
4. Add notes and select appropriate customer type

### 3. Test Data Export

#### CSV Export:
1. Go to the dashboard: http://127.0.0.1:8001/
2. Click the "Export CSV" button
3. Download will include all customer data with all enhanced fields
4. Filename format: `customers_export_YYYYMMDD_HHMMSS.csv`

#### Data Verification:
- Verify all entered data appears in the CSV export
- Check that all enhanced fields are properly exported
- Confirm data integrity and formatting

### 4. Test Additional Field Requirements

#### To Add Custom Fields:
```bash
# Example: Add a custom field for "Emergency Contact"
python manage.py add_custom_field --field-name "emergency_contact" --field-type "CharField" --max-length 200 --blank --null

# Run the migration
python manage.py migrate

# Get instructions for updating forms and admin
python manage.py update_customer_interface
```

#### Supported Field Types:
- CharField (text with max length)
- TextField (longer text)
- EmailField (email validation)
- URLField (URL validation)
- IntegerField (numbers)
- DateField (dates)
- BooleanField (true/false)

### 5. Communication Channel Testing

#### Multiple Communication Preferences:
1. Create customers with different preferred communication methods
2. Test the CustomerCommunicationPreference model for multiple channels
3. Verify priority-based communication setup

### 6. Admin Interface Testing

#### Advanced Admin Features:
1. Go to http://127.0.0.1:8001/admin/
2. Login with admin credentials
3. Test the enhanced Customer admin with:
   - Multiple fieldsets for organization
   - Inline communication preferences
   - Advanced search capabilities
   - Filter options

### 7. API Testing

#### REST API Endpoints:
- **Customers**: http://127.0.0.1:8001/api/v1/customers/
- **CSV Export**: http://127.0.0.1:8001/api/v1/customers/export_csv/
- **Search**: http://127.0.0.1:8001/api/v1/customers/search_by_contact/?contact=example

### 8. Data Validation Testing

#### Test Cases:
1. **Required Fields**: Try submitting with missing required fields
2. **Email Validation**: Enter invalid email formats
3. **Phone Formats**: Test various phone number formats
4. **URL Validation**: Test company website and social media URLs
5. **Date Validation**: Test date of birth with various formats

### 9. Performance Testing

#### Load Testing:
1. Create multiple customers (10-50 for initial testing)
2. Test CSV export with larger datasets
3. Verify search functionality with multiple records
4. Test admin interface responsiveness

### 10. Backup and Recovery

#### Git Operations:
```bash
# Check current status
git status

# Create backup before major changes
git add .
git commit -m "UAT testing checkpoint - [describe changes]"
git push origin main
```

## Troubleshooting

### Common Issues:
1. **Migration Errors**: Run `python manage.py showmigrations` to check status
2. **Form Errors**: Check browser console for JavaScript errors
3. **CSV Export Issues**: Verify all fields are properly defined in the export view
4. **Admin Access**: Ensure superuser is created: `python manage.py createsuperuser`

### Debug Commands:
```bash
# Check Django status
python manage.py check

# Show model fields
python manage.py show_customer_fields

# Database shell
python manage.py shell

# View logs
tail -f /path/to/django.log
```

## Success Criteria

✅ **Data Entry**: All enhanced fields accept and save data correctly
✅ **Data Retrieval**: Data can be viewed in admin and customer detail pages
✅ **CSV Export**: Complete data export with all fields
✅ **Field Addition**: Custom fields can be added using management commands
✅ **Communication**: Multiple communication channels properly configured
✅ **Validation**: Form validation works for all field types
✅ **Performance**: System responds quickly with test data volume

## Next Steps After UAT

1. **Production Deployment**: Prepare for production environment
2. **User Training**: Train end users on new features
3. **Data Migration**: Import existing customer data if needed
4. **Monitoring**: Set up logging and monitoring for production
5. **Backup Strategy**: Implement regular backup procedures
