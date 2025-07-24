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
    first_name = models.CharField(max_length=100, help_text="Given name/First name")
    middle_name = models.CharField(max_length=100, blank=True, help_text="Middle name(s)")
    last_name = models.CharField(max_length=100, help_text="Family name/Last name/Surname")
    preferred_name = models.CharField(max_length=100, blank=True, help_text="Nickname or preferred name")
    name_suffix = models.CharField(max_length=20, blank=True, help_text="Jr., Sr., III, etc.")
    
    # Multiple Email Addresses
    email_primary = models.EmailField(unique=True, validators=[EmailValidator()], help_text="Primary email address")
    email_secondary = models.EmailField(blank=True, validators=[EmailValidator()], help_text="Secondary email address")
    
    # Multiple Phone Numbers with country codes
    phone_primary = models.CharField(max_length=20, blank=True, help_text="Primary phone number with country code")
    phone_primary_country_code = models.CharField(max_length=5, blank=True, help_text="Country code for primary phone")
    phone_secondary = models.CharField(max_length=20, blank=True, help_text="Secondary phone number with country code")
    phone_secondary_country_code = models.CharField(max_length=5, blank=True, help_text="Country code for secondary phone")
    fax = models.CharField(max_length=20, blank=True, help_text="Fax number")
    fax_country_code = models.CharField(max_length=5, blank=True, help_text="Country code for fax")
    
    # Messaging Apps
    whatsapp_number = models.CharField(max_length=20, blank=True)
    whatsapp_country_code = models.CharField(max_length=5, blank=True, help_text="Country code for WhatsApp")
    wechat_id = models.CharField(max_length=100, blank=True)
    
    # Social Media Accounts
    linkedin_profile = models.URLField(blank=True, validators=[URLValidator()], help_text="LinkedIn profile URL")
    facebook_profile = models.URLField(blank=True, validators=[URLValidator()], help_text="Facebook profile URL")
    twitter_handle = models.CharField(max_length=100, blank=True, help_text="Twitter/X handle (without @)")
    instagram_handle = models.CharField(max_length=100, blank=True, help_text="Instagram handle (without @)")
    
    # Geographic Information with comprehensive country/region choices
    COUNTRY_CHOICES = [
        ('', 'Select Country/Region'),
        # Asia Pacific
        ('CN', 'China'),
        ('HK', 'Hong Kong SAR'),
        ('TW', 'Taiwan'),
        ('MO', 'Macau SAR'),
        ('SG', 'Singapore'),
        ('MY', 'Malaysia'),
        ('TH', 'Thailand'),
        ('VN', 'Vietnam'),
        ('PH', 'Philippines'),
        ('ID', 'Indonesia'),
        ('KR', 'South Korea'),
        ('JP', 'Japan'),
        ('IN', 'India'),
        ('AU', 'Australia'),
        ('NZ', 'New Zealand'),
        # Europe
        ('GB', 'United Kingdom'),
        ('DE', 'Germany'),
        ('FR', 'France'),
        ('IT', 'Italy'),
        ('ES', 'Spain'),
        ('NL', 'Netherlands'),
        ('BE', 'Belgium'),
        ('CH', 'Switzerland'),
        ('AT', 'Austria'),
        ('SE', 'Sweden'),
        ('NO', 'Norway'),
        ('DK', 'Denmark'),
        ('FI', 'Finland'),
        # Americas
        ('US', 'United States'),
        ('CA', 'Canada'),
        ('MX', 'Mexico'),
        ('BR', 'Brazil'),
        ('AR', 'Argentina'),
        ('CL', 'Chile'),
        ('CO', 'Colombia'),
        ('PE', 'Peru'),
        # Middle East & Africa
        ('AE', 'United Arab Emirates'),
        ('SA', 'Saudi Arabia'),
        ('IL', 'Israel'),
        ('ZA', 'South Africa'),
        ('EG', 'Egypt'),
        ('KE', 'Kenya'),
        ('NG', 'Nigeria'),
        # Others
        ('RU', 'Russia'),
        ('TR', 'Turkey'),
        ('OTHER', 'Other (please specify in notes)'),
    ]
    
    country_region = models.CharField(
        max_length=10, 
        choices=COUNTRY_CHOICES, 
        blank=True, 
        help_text="Select your country or region"
    )
    
    # Country code mapping for phone numbers
    COUNTRY_CODE_MAP = {
        'CN': '+86', 'HK': '+852', 'TW': '+886', 'MO': '+853',
        'SG': '+65', 'MY': '+60', 'TH': '+66', 'VN': '+84',
        'PH': '+63', 'ID': '+62', 'KR': '+82', 'JP': '+81',
        'IN': '+91', 'AU': '+61', 'NZ': '+64',
        'GB': '+44', 'DE': '+49', 'FR': '+33', 'IT': '+39',
        'ES': '+34', 'NL': '+31', 'BE': '+32', 'CH': '+41',
        'AT': '+43', 'SE': '+46', 'NO': '+47', 'DK': '+45', 'FI': '+358',
        'US': '+1', 'CA': '+1', 'MX': '+52', 'BR': '+55',
        'AR': '+54', 'CL': '+56', 'CO': '+57', 'PE': '+51',
        'AE': '+971', 'SA': '+966', 'IL': '+972', 'ZA': '+27',
        'EG': '+20', 'KE': '+254', 'NG': '+234',
        'RU': '+7', 'TR': '+90',
    }
    
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
        full_name = f"{self.first_name} {self.last_name}"
        if self.preferred_name:
            full_name = f"{self.preferred_name} ({full_name})"
        return f"{full_name} ({self.email_primary})"
    
    @property
    def full_name(self):
        """Get complete formatted name"""
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        if self.name_suffix:
            parts.append(self.name_suffix)
        return ' '.join(parts)
    
    @property
    def display_name(self):
        """Get display name (preferred name or full name)"""
        if self.preferred_name:
            return self.preferred_name
        return f"{self.first_name} {self.last_name}"
    
    def get_country_code(self):
        """Get country code for the selected country/region"""
        if self.country_region and self.country_region in self.COUNTRY_CODE_MAP:
            return self.COUNTRY_CODE_MAP[self.country_region]
        return ''
    
    def auto_set_country_codes(self):
        """Automatically set country codes based on selected country"""
        country_code = self.get_country_code()
        if country_code:
            if not self.phone_primary_country_code and self.phone_primary:
                self.phone_primary_country_code = country_code
            if not self.phone_secondary_country_code and self.phone_secondary:
                self.phone_secondary_country_code = country_code
            if not self.whatsapp_country_code and self.whatsapp_number:
                self.whatsapp_country_code = country_code
            if not self.fax_country_code and self.fax:
                self.fax_country_code = country_code
    
    def save(self, *args, **kwargs):
        """Override save to automatically set country codes"""
        self.auto_set_country_codes()
        super().save(*args, **kwargs)
    
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