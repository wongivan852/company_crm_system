#!/usr/bin/env python
"""
Direct YouTube data test - bypasses all forms and web interface
Run this with: python manage.py shell < direct_youtube_test.py
"""

from crm.models import Customer
import uuid

print("🧪 DIRECT YOUTUBE DATA TEST")
print("="*50)

try:
    # Create customer directly in database
    customer = Customer(
        first_name='YouTube',
        last_name='Test',
        email_primary=f'youtube_test_{uuid.uuid4().hex[:8]}@example.com',
        customer_type='individual',
        status='prospect', 
        preferred_communication_method='email',
        youtube_handle='robbybranham'
    )
    
    print(f"📝 Creating customer with:")
    print(f"   Name: {customer.first_name} {customer.last_name}")
    print(f"   Email: {customer.email_primary}")
    print(f"   YouTube Handle: {customer.youtube_handle}")
    
    # Validate and save
    customer.full_clean()
    customer.save()
    
    print(f"✅ SUCCESS!")
    print(f"   Customer ID: {customer.id}")
    print(f"   YouTube Handle: @{customer.youtube_handle}")
    print(f"   Auto-generated URL: {customer.youtube_channel_url}")
    print(f"   Created: {customer.created_at}")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    print(f"🔍 Full traceback:\n{traceback.format_exc()}")

print("\n" + "="*50)
print("🔍 Testing complete!")