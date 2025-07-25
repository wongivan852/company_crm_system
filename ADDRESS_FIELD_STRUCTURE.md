# 📍 Address Field Structure Documentation

## Address Field Resolution

The Customer model previously had conflicting address definitions that have been resolved.

## Current Address Fields

### Primary Address Fields
- **`address_primary`** (`TextField`): Complete primary address (Home/Office)
- **`address_secondary`** (`TextField`): Complete secondary address (Mailing/Alternative)

### Individual Address Components
- **`address`** (`CharField`): Street address component
- **`city`** (`CharField`): City
- **`state_province`** (`CharField`): State or Province  
- **`postal_code`** (`CharField`): Postal/ZIP code
- **`country_region`** (`CharField`): Country/Region code

## Usage Guidelines

### For Complete Addresses
Use `address_primary` and `address_secondary` for storing complete address text:
```python
customer.address_primary = "123 Main St, Apt 4B\nNew York, NY 10001\nUnited States"
customer.address_secondary = "PO Box 456\nNew York, NY 10002\nUnited States"
```

### For Structured Address Components
Use individual fields for structured address data:
```python
customer.address = "123 Main St, Apt 4B"
customer.city = "New York"
customer.state_province = "NY"
customer.postal_code = "10001"
customer.country_region = "US"
```

## Form Integration

The CustomerForm includes all address fields:
```python
fields = [
    # ... other fields ...
    'country_region',
    'address', 'city', 'state_province', 'postal_code',  # Components
    'address_primary', 'address_secondary',  # Complete addresses
    # ... other fields ...
]
```

## Migration History

1. **Initial**: Had generic `address` field
2. **Enhancement**: Added `address_primary` and `address_secondary`
3. **Components**: Added `city`, `state_province`, `postal_code`
4. **Conflict Resolution**: Removed conflicting `@property` for `address`

## Best Practices

### Frontend Forms
- Use structured components (`address`, `city`, etc.) for user input
- Auto-populate `address_primary` from components if needed
- Allow manual override of `address_primary` for complex addresses

### API Responses
- Include both structured and complete address fields
- Let clients choose appropriate format

### Data Export
- Export all address fields for maximum flexibility
- Include country codes for international compatibility

## Backward Compatibility

✅ **Maintained**: All existing address data preserved
✅ **Enhanced**: New structured address components available
✅ **Flexible**: Supports both structured and free-form addresses

## Migration Impact

No data loss - all existing address data remains intact in their respective fields.