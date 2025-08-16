#!/usr/bin/env python
import os
import sys
import django

# Add the project root to the Python path
sys.path.append('/Users/wongivan/company_crm_system/crm_project')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')

# Setup Django
django.setup()

from crm.models import Customer
from datetime import date

def test_data_saving():
    print("🔍 Testing data saving functionality...")
    
    # Count existing customers
    initial_count = Customer.objects.count()
    print(f"📊 Initial customer count: {initial_count}")
    
    # Create a test customer
    test_customer = Customer(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        company_name="Test Company",
        country_region="US",
        facebook_profile="https://www.facebook.com/testuser"
    )
    
    try:
        test_customer.save()
        print("✅ Test customer saved successfully!")
        
        # Verify it was saved
        final_count = Customer.objects.count()
        print(f"📊 Final customer count: {final_count}")
        
        if final_count > initial_count:
            print("✅ Data saving is working correctly!")
            
            # Show the saved customer
            saved_customer = Customer.objects.get(email="test@example.com")
            print(f"📋 Saved customer: {saved_customer.first_name} {saved_customer.last_name}")
            print(f"📘 Facebook profile: {saved_customer.facebook_profile}")
            
            # Clean up test data
            saved_customer.delete()
            print("🧹 Test customer cleaned up")
            
        else:
            print("❌ Data was not saved properly")
            
    except Exception as e:
        print(f"❌ Error saving customer: {e}")

if __name__ == "__main__":
    test_data_saving()
