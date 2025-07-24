# models.py - Core CRM Models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, URLValidator
import uuid

class Customer(models.Model):
    CUSTOMER_TYPES = [
        ('individual', 'Individual Learner'),
        ('corporate', 'Corporate Client'),
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('prospect', 'Prospect'),
        ('alumni', 'Alumni'),
    ]
    
    # Core Identity
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    # Multiple Email Addresses
    email_primary = models.EmailField(unique=True, validators=[EmailValidator()], help_text="Primary email address")
    email_secondary = models.EmailField(blank=True, validators=[EmailValidator()], help_text="Secondary email address")
    
    # Multiple Phone Numbers
    phone_primary = models.CharField(max_length=20, blank=True, help_text="Primary phone number")
    phone_secondary = models.CharField(max_length=20, blank=True, help_text="Secondary phone number")
    fax = models.CharField(max_length=20, blank=True, help_text="Fax number")
    
    # Messaging Apps
    whatsapp_number = models.CharField(max_length=20, blank=True)
    wechat_id = models.CharField(max_length=100, blank=True)
    
    # Social Media Accounts
    linkedin_profile = models.URLField(blank=True, validators=[URLValidator()], help_text="LinkedIn profile URL")
    facebook_profile = models.URLField(blank=True, validators=[URLValidator()], help_text="Facebook profile URL")
    twitter_handle = models.CharField(max_length=100, blank=True, help_text="Twitter/X handle (without @)")
    instagram_handle = models.CharField(max_length=100, blank=True, help_text="Instagram handle (without @)")
    
    # Geographic Information
    country_region = models.CharField(max_length=100, blank=True, help_text="Country/Region")
    
    # Customer Classification
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='prospect')
    
    # Professional Information (Multiple positions for career progression)
    company_primary = models.CharField(max_length=200, blank=True, help_text="Current/Primary company")
    position_primary = models.CharField(max_length=100, blank=True, help_text="Current/Primary position")
    company_secondary = models.CharField(max_length=200, blank=True, help_text="Secondary/Previous company")
    position_secondary = models.CharField(max_length=100, blank=True, help_text="Secondary/Previous position")
    company_website = models.URLField(blank=True, validators=[URLValidator()], help_text="Company website")
    
    # Multiple Addresses
    address_primary = models.TextField(blank=True, help_text="Primary address (Home/Office)")
    address_secondary = models.TextField(blank=True, help_text="Secondary address (Mailing/Alternative)")
    
    # Learning preferences
    preferred_learning_format = models.CharField(max_length=50, blank=True)
    interests = models.TextField(blank=True, help_text="Comma-separated interests")
    
    # Marketing Consent
    marketing_consent = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email_primary})"
    
    @property
    def email(self):
        """Backward compatibility property for primary email"""
        return self.email_primary
    
    @property 
    def phone_number(self):
        """Backward compatibility property for primary phone"""
        return self.phone_primary
    
    @property
    def company(self):
        """Backward compatibility property for primary company"""
        return self.company_primary
    
    @property
    def position(self):
        """Backward compatibility property for primary position"""
        return self.position_primary
    
    @property
    def address(self):
        """Backward compatibility property for primary address"""
        return self.address_primary


class CustomerCommunicationPreference(models.Model):
    """Model to handle multiple communication preferences per customer"""
    
    COMMUNICATION_TYPES = [
        ('email_primary', 'Primary Email'),
        ('email_secondary', 'Secondary Email'),
        ('phone_primary', 'Primary Phone'),
        ('phone_secondary', 'Secondary Phone'),
        ('whatsapp', 'WhatsApp'),
        ('wechat', 'WeChat'),
        ('linkedin', 'LinkedIn'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter/X'),
        ('instagram', 'Instagram'),
        ('fax', 'Fax'),
    ]
    
    PRIORITY_CHOICES = [
        (1, 'Primary'),
        (2, 'Secondary'),
        (3, 'Tertiary'),
        (4, 'Emergency Only'),
        (5, 'Do Not Use'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='communication_preferences')
    communication_type = models.CharField(max_length=20, choices=COMMUNICATION_TYPES)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    is_active = models.BooleanField(default=True)
    notes = models.CharField(max_length=200, blank=True, help_text="e.g., 'Work hours only', 'Weekends preferred'")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['customer', 'communication_type']
        ordering = ['customer', 'priority', 'communication_type']
    
    def __str__(self):
        return f"{self.customer} - {self.get_communication_type_display()} (Priority {self.priority})"

class Course(models.Model):
    COURSE_TYPES = [
        ('online', 'Online Course'),
        ('offline', 'In-Person Course'),
        ('hybrid', 'Hybrid Course'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    course_type = models.CharField(max_length=20, choices=COURSE_TYPES)
    duration_hours = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_participants = models.PositiveIntegerField()
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_deadline = models.DateTimeField()
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ], default='pending')
    
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['customer', 'course']
    
    def __str__(self):
        return f"{self.customer} - {self.course}"

class Conference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    venue = models.CharField(max_length=300)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2)
    max_attendees = models.PositiveIntegerField()
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class ConferenceRegistration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    special_requirements = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['customer', 'conference']

class CommunicationLog(models.Model):
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('wechat', 'WeChat'),
        ('phone', 'Phone'),
        ('in_person', 'In Person'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_outbound = models.BooleanField(default=True)  # True for sent, False for received
    
    # External message IDs for tracking
    external_message_id = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.customer} - {self.channel} - {self.subject}"