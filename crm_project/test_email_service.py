#!/usr/bin/env python
"""
Test script to demonstrate the enhanced email service functionality.
Run this script to test email templates and campaigns.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')
django.setup()

from crm.models import Customer, EmailTemplate, EmailCampaign
from crm.email_service import EnhancedEmailService, send_welcome_email
from django.utils import timezone

def test_email_service():
    """Test the enhanced email service"""
    print("=== Testing Enhanced Email Service ===\n")
    
    # Initialize service
    email_service = EnhancedEmailService()
    
    # Get a test customer
    customer = Customer.objects.first()
    if not customer:
        print("❌ No customers found. Please add some customers first.")
        return
    
    print(f"Testing with customer: {customer.full_name} ({customer.email_primary})")
    
    # Test 1: Send welcome email using template
    print("\n1. Testing Welcome Email with Template:")
    try:
        success, message = send_welcome_email(customer)
        if success:
            print(f"✅ Welcome email sent successfully: {message}")
        else:
            print(f"❌ Welcome email failed: {message}")
    except Exception as e:
        print(f"❌ Welcome email error: {str(e)}")
    
    # Test 2: Get email analytics
    print("\n2. Testing Email Analytics:")
    try:
        analytics = email_service.get_email_analytics(days=30)
        print(f"✅ Email Analytics (Last 30 days):")
        print(f"   - Total Emails: {analytics['total_emails']}")
        print(f"   - Sent: {analytics['sent']}")
        print(f"   - Open Rate: {analytics['open_rate']}%")
        print(f"   - Click Rate: {analytics['click_rate']}%")
        print(f"   - Bounce Rate: {analytics['bounce_rate']}%")
    except Exception as e:
        print(f"❌ Analytics error: {str(e)}")
    
    # Test 3: Create and test campaign
    print("\n3. Testing Email Campaign:")
    try:
        # Get welcome template
        template = EmailTemplate.objects.filter(template_type='welcome', status='active').first()
        if template:
            # Create test campaign
            campaign = email_service.campaign_service.create_campaign(
                name='Test Welcome Campaign',
                description='Test campaign for new customers',
                template=template,
                target_audience='prospects',  # or 'all_customers'
                created_by='Test Script'
            )
            
            print(f"✅ Created campaign: {campaign.name}")
            print(f"   - Target Recipients: {campaign.total_recipients}")
            
            # Uncomment the following lines to actually send the campaign
            # WARNING: This will send real emails!
            """
            if campaign.total_recipients > 0:
                results = email_service.send_campaign(campaign)
                print(f"   - Emails Sent: {results['emails_sent']}")
                print(f"   - Emails Failed: {results['emails_failed']}")
            """
            print("   (Campaign created but not sent - uncomment code to send)")
        else:
            print("❌ No welcome template found")
    except Exception as e:
        print(f"❌ Campaign error: {str(e)}")
    
    # Test 4: Template rendering
    print("\n4. Testing Template Rendering:")
    try:
        template = EmailTemplate.objects.filter(template_type='welcome', status='active').first()
        if template:
            variables = email_service.template_service.get_customer_variables(customer)
            rendered_subject = email_service.template_service.render_template(template.subject, variables)
            print(f"✅ Template rendering successful:")
            print(f"   - Original subject: {template.subject}")
            print(f"   - Rendered subject: {rendered_subject}")
        else:
            print("❌ No template found for testing")
    except Exception as e:
        print(f"❌ Template rendering error: {str(e)}")
    
    print("\n=== Email Service Test Complete ===")

def show_email_templates():
    """Display available email templates"""
    print("\n=== Available Email Templates ===")
    templates = EmailTemplate.objects.filter(status='active')
    
    if not templates.exists():
        print("No active templates found.")
        return
    
    for template in templates:
        print(f"\n📧 {template.name}")
        print(f"   Type: {template.get_template_type_display()}")
        print(f"   Subject: {template.subject}")
        print(f"   Usage Count: {template.usage_count}")
        if template.last_used:
            print(f"   Last Used: {template.last_used}")

def show_recent_campaigns():
    """Display recent email campaigns"""
    print("\n=== Recent Email Campaigns ===")
    campaigns = EmailCampaign.objects.all().order_by('-created_at')[:5]
    
    if not campaigns.exists():
        print("No campaigns found.")
        return
    
    for campaign in campaigns:
        print(f"\n📨 {campaign.name}")
        print(f"   Status: {campaign.get_status_display()}")
        print(f"   Target: {campaign.get_target_audience_display()}")
        print(f"   Recipients: {campaign.total_recipients}")
        print(f"   Sent: {campaign.emails_sent}")
        if campaign.emails_sent > 0:
            print(f"   Open Rate: {campaign.open_rate}%")
            print(f"   Click Rate: {campaign.click_rate}%")

if __name__ == '__main__':
    try:
        show_email_templates()
        show_recent_campaigns()
        test_email_service()
    except Exception as e:
        print(f"❌ Test script error: {str(e)}")
        import traceback
        traceback.print_exc()