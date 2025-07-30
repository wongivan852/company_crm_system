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
    first_name = models.CharField(max_length=100, blank=True, help_text="Given name/First name (optional)")
    middle_name = models.CharField(max_length=100, blank=True, help_text="Middle name(s)")
    last_name = models.CharField(max_length=100, help_text="Family name/Last name/Surname")
    preferred_name = models.CharField(max_length=100, blank=True, help_text="Nickname or preferred name")
    name_suffix = models.CharField(max_length=20, blank=True, help_text="Jr., Sr., III, etc.")
    
    # Additional Names and Identity
    maiden_name = models.CharField(max_length=100, blank=True, help_text="Maiden name (if applicable)")
    other_names = models.CharField(max_length=200, blank=True, help_text="Other names, aliases, or previous names")
    title = models.CharField(max_length=50, blank=True, help_text="Title (Dr., Prof., Mr., Ms., etc.)")
    
    # Professional Designation
    DESIGNATION_CHOICES = [
        ('', 'Select Designation'),
        # Academic Titles
        ('professor', 'Professor'),
        ('prof', 'Prof.'),
        ('dr', 'Dr.'),
        ('phd', 'Ph.D.'),
        ('doctorate', 'Doctorate'),
        ('professor_emeritus', 'Professor Emeritus'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
        ('senior_lecturer', 'Senior Lecturer'),
        # Engineering Titles
        ('ir', 'Ir.'),
        ('eng', 'Eng.'),
        ('pe', 'P.E.'),
        ('eit', 'E.I.T.'),
        # Medical Titles
        ('md', 'M.D.'),
        ('do', 'D.O.'),
        ('dds', 'D.D.S.'),
        ('dvm', 'D.V.M.'),
        # Legal Titles  
        ('jd', 'J.D.'),
        ('esquire', 'Esq.'),
        # Business/Professional
        ('cpa', 'C.P.A.'),
        ('cfa', 'C.F.A.'),
        ('pmp', 'P.M.P.'),
        ('mba', 'M.B.A.'),
        # Religious
        ('rev', 'Rev.'),
        ('father', 'Father'),
        ('pastor', 'Pastor'),
        # Military
        ('captain', 'Captain'),
        ('colonel', 'Colonel'),
        ('major', 'Major'),
        ('general', 'General'),
        # Other
        ('other', 'Other'),
    ]
    designation = models.CharField(
        max_length=50, 
        choices=DESIGNATION_CHOICES, 
        blank=True, 
        help_text="Professional or academic designation"
    )
    
    # Personal Details
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, help_text="Gender")
    date_of_birth = models.DateField(blank=True, null=True, help_text="Date of birth")
    nationality = models.CharField(max_length=100, blank=True, help_text="Nationality")
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=200, blank=True, help_text="Emergency contact full name")
    emergency_contact_relationship = models.CharField(max_length=100, blank=True, help_text="Relationship to emergency contact")
    emergency_contact_phone = models.CharField(max_length=20, blank=True, help_text="Emergency contact phone number")
    emergency_contact_email = models.EmailField(blank=True, help_text="Emergency contact email")
    
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
        # Africa
        ('DZ', 'Algeria'),
        ('AO', 'Angola'),
        ('BJ', 'Benin'),
        ('BW', 'Botswana'),
        ('BF', 'Burkina Faso'),
        ('BI', 'Burundi'),
        ('CM', 'Cameroon'),
        ('CV', 'Cape Verde'),
        ('CF', 'Central African Republic'),
        ('TD', 'Chad'),
        ('KM', 'Comoros'),
        ('CG', 'Congo'),
        ('CD', 'Congo (Democratic Republic)'),
        ('CI', 'Côte d\'Ivoire'),
        ('DJ', 'Djibouti'),
        ('EG', 'Egypt'),
        ('GQ', 'Equatorial Guinea'),
        ('ER', 'Eritrea'),
        ('ET', 'Ethiopia'),
        ('GA', 'Gabon'),
        ('GM', 'Gambia'),
        ('GH', 'Ghana'),
        ('GN', 'Guinea'),
        ('GW', 'Guinea-Bissau'),
        ('KE', 'Kenya'),
        ('LS', 'Lesotho'),
        ('LR', 'Liberia'),
        ('LY', 'Libya'),
        ('MG', 'Madagascar'),
        ('MW', 'Malawi'),
        ('ML', 'Mali'),
        ('MR', 'Mauritania'),
        ('MU', 'Mauritius'),
        ('MA', 'Morocco'),
        ('MZ', 'Mozambique'),
        ('NA', 'Namibia'),
        ('NE', 'Niger'),
        ('NG', 'Nigeria'),
        ('RW', 'Rwanda'),
        ('ST', 'São Tomé and Príncipe'),
        ('SN', 'Senegal'),
        ('SC', 'Seychelles'),
        ('SL', 'Sierra Leone'),
        ('SO', 'Somalia'),
        ('ZA', 'South Africa'),
        ('SS', 'South Sudan'),
        ('SD', 'Sudan'),
        ('SZ', 'Swaziland'),
        ('TZ', 'Tanzania'),
        ('TG', 'Togo'),
        ('TN', 'Tunisia'),
        ('UG', 'Uganda'),
        ('ZM', 'Zambia'),
        ('ZW', 'Zimbabwe'),
        
        # Antarctica
        ('AQ', 'Antarctica'),
        
        # Asia
        ('AF', 'Afghanistan'),
        ('AM', 'Armenia'),
        ('AZ', 'Azerbaijan'),
        ('BH', 'Bahrain'),
        ('BD', 'Bangladesh'),
        ('BT', 'Bhutan'),
        ('BN', 'Brunei'),
        ('KH', 'Cambodia'),
        ('CN', 'China'),
        ('CY', 'Cyprus'),
        ('GE', 'Georgia'),
        ('HK', 'Hong Kong SAR'),
        ('IN', 'India'),
        ('ID', 'Indonesia'),
        ('IR', 'Iran'),
        ('IQ', 'Iraq'),
        ('IL', 'Israel'),
        ('JP', 'Japan'),
        ('JO', 'Jordan'),
        ('KZ', 'Kazakhstan'),
        ('KW', 'Kuwait'),
        ('KG', 'Kyrgyzstan'),
        ('LA', 'Laos'),
        ('LB', 'Lebanon'),
        ('MO', 'Macau SAR'),
        ('MY', 'Malaysia'),
        ('MV', 'Maldives'),
        ('MN', 'Mongolia'),
        ('MM', 'Myanmar'),
        ('NP', 'Nepal'),
        ('KP', 'North Korea'),
        ('OM', 'Oman'),
        ('PK', 'Pakistan'),
        ('PS', 'Palestine'),
        ('PH', 'Philippines'),
        ('QA', 'Qatar'),
        ('SA', 'Saudi Arabia'),
        ('SG', 'Singapore'),
        ('KR', 'South Korea'),
        ('LK', 'Sri Lanka'),
        ('SY', 'Syria'),
        ('TW', 'Taiwan'),
        ('TJ', 'Tajikistan'),
        ('TH', 'Thailand'),
        ('TL', 'Timor-Leste'),
        ('TR', 'Turkey'),
        ('TM', 'Turkmenistan'),
        ('AE', 'United Arab Emirates'),
        ('UZ', 'Uzbekistan'),
        ('VN', 'Vietnam'),
        ('YE', 'Yemen'),
        
        # Europe
        ('AL', 'Albania'),
        ('AD', 'Andorra'),
        ('AT', 'Austria'),
        ('BY', 'Belarus'),
        ('BE', 'Belgium'),
        ('BA', 'Bosnia and Herzegovina'),
        ('BG', 'Bulgaria'),
        ('HR', 'Croatia'),
        ('CZ', 'Czech Republic'),
        ('DK', 'Denmark'),
        ('EE', 'Estonia'),
        ('FI', 'Finland'),
        ('FR', 'France'),
        ('DE', 'Germany'),
        ('GR', 'Greece'),
        ('HU', 'Hungary'),
        ('IS', 'Iceland'),
        ('IE', 'Ireland'),
        ('IT', 'Italy'),
        ('XK', 'Kosovo'),
        ('LV', 'Latvia'),
        ('LI', 'Liechtenstein'),
        ('LT', 'Lithuania'),
        ('LU', 'Luxembourg'),
        ('MK', 'Macedonia'),
        ('MT', 'Malta'),
        ('MD', 'Moldova'),
        ('MC', 'Monaco'),
        ('ME', 'Montenegro'),
        ('NL', 'Netherlands'),
        ('NO', 'Norway'),
        ('PL', 'Poland'),
        ('PT', 'Portugal'),
        ('RO', 'Romania'),
        ('RU', 'Russia'),
        ('SM', 'San Marino'),
        ('RS', 'Serbia'),
        ('SK', 'Slovakia'),
        ('SI', 'Slovenia'),
        ('ES', 'Spain'),
        ('SE', 'Sweden'),
        ('CH', 'Switzerland'),
        ('UA', 'Ukraine'),
        ('GB', 'United Kingdom'),
        ('VA', 'Vatican City'),
        
        # North America
        ('AG', 'Antigua and Barbuda'),
        ('BS', 'Bahamas'),
        ('BB', 'Barbados'),
        ('BZ', 'Belize'),
        ('CA', 'Canada'),
        ('CR', 'Costa Rica'),
        ('CU', 'Cuba'),
        ('DM', 'Dominica'),
        ('DO', 'Dominican Republic'),
        ('SV', 'El Salvador'),
        ('GD', 'Grenada'),
        ('GT', 'Guatemala'),
        ('HT', 'Haiti'),
        ('HN', 'Honduras'),
        ('JM', 'Jamaica'),
        ('MX', 'Mexico'),
        ('NI', 'Nicaragua'),
        ('PA', 'Panama'),
        ('KN', 'Saint Kitts and Nevis'),
        ('LC', 'Saint Lucia'),
        ('VC', 'Saint Vincent and the Grenadines'),
        ('TT', 'Trinidad and Tobago'),
        ('US', 'United States'),
        
        # Oceania
        ('AU', 'Australia'),
        ('FJ', 'Fiji'),
        ('KI', 'Kiribati'),
        ('MH', 'Marshall Islands'),
        ('FM', 'Micronesia'),
        ('NR', 'Nauru'),
        ('NZ', 'New Zealand'),
        ('PW', 'Palau'),
        ('PG', 'Papua New Guinea'),
        ('WS', 'Samoa'),
        ('SB', 'Solomon Islands'),
        ('TO', 'Tonga'),
        ('TV', 'Tuvalu'),
        ('VU', 'Vanuatu'),
        
        # South America
        ('AR', 'Argentina'),
        ('BO', 'Bolivia'),
        ('BR', 'Brazil'),
        ('CL', 'Chile'),
        ('CO', 'Colombia'),
        ('EC', 'Ecuador'),
        ('GY', 'Guyana'),
        ('PY', 'Paraguay'),
        ('PE', 'Peru'),
        ('SR', 'Suriname'),
        ('UY', 'Uruguay'),
        ('VE', 'Venezuela'),
        
        # Others
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
        # Africa
        'DZ': '+213', 'AO': '+244', 'BJ': '+229', 'BW': '+267', 'BF': '+226', 'BI': '+257',
        'CM': '+237', 'CV': '+238', 'CF': '+236', 'TD': '+235', 'KM': '+269', 'CG': '+242',
        'CD': '+243', 'CI': '+225', 'DJ': '+253', 'EG': '+20', 'GQ': '+240', 'ER': '+291',
        'ET': '+251', 'GA': '+241', 'GM': '+220', 'GH': '+233', 'GN': '+224', 'GW': '+245',
        'KE': '+254', 'LS': '+266', 'LR': '+231', 'LY': '+218', 'MG': '+261', 'MW': '+265',
        'ML': '+223', 'MR': '+222', 'MU': '+230', 'MA': '+212', 'MZ': '+258', 'NA': '+264',
        'NE': '+227', 'NG': '+234', 'RW': '+250', 'ST': '+239', 'SN': '+221', 'SC': '+248',
        'SL': '+232', 'SO': '+252', 'ZA': '+27', 'SS': '+211', 'SD': '+249', 'SZ': '+268',
        'TZ': '+255', 'TG': '+228', 'TN': '+216', 'UG': '+256', 'ZM': '+260', 'ZW': '+263',
        
        # Asia
        'AF': '+93', 'AM': '+374', 'AZ': '+994', 'BH': '+973', 'BD': '+880', 'BT': '+975',
        'BN': '+673', 'KH': '+855', 'CN': '+86', 'CY': '+357', 'GE': '+995', 'HK': '+852',
        'IN': '+91', 'ID': '+62', 'IR': '+98', 'IQ': '+964', 'IL': '+972', 'JP': '+81',
        'JO': '+962', 'KZ': '+7', 'KW': '+965', 'KG': '+996', 'LA': '+856', 'LB': '+961',
        'MO': '+853', 'MY': '+60', 'MV': '+960', 'MN': '+976', 'MM': '+95', 'NP': '+977',
        'KP': '+850', 'OM': '+968', 'PK': '+92', 'PS': '+970', 'PH': '+63', 'QA': '+974',
        'SA': '+966', 'SG': '+65', 'KR': '+82', 'LK': '+94', 'SY': '+963', 'TW': '+886',
        'TJ': '+992', 'TH': '+66', 'TL': '+670', 'TR': '+90', 'TM': '+993', 'AE': '+971',
        'UZ': '+998', 'VN': '+84', 'YE': '+967',
        
        # Europe
        'AL': '+355', 'AD': '+376', 'AT': '+43', 'BY': '+375', 'BE': '+32', 'BA': '+387',
        'BG': '+359', 'HR': '+385', 'CZ': '+420', 'DK': '+45', 'EE': '+372', 'FI': '+358',
        'FR': '+33', 'DE': '+49', 'GR': '+30', 'HU': '+36', 'IS': '+354', 'IE': '+353',
        'IT': '+39', 'XK': '+383', 'LV': '+371', 'LI': '+423', 'LT': '+370', 'LU': '+352',
        'MK': '+389', 'MT': '+356', 'MD': '+373', 'MC': '+377', 'ME': '+382', 'NL': '+31',
        'NO': '+47', 'PL': '+48', 'PT': '+351', 'RO': '+40', 'RU': '+7', 'SM': '+378',
        'RS': '+381', 'SK': '+421', 'SI': '+386', 'ES': '+34', 'SE': '+46', 'CH': '+41',
        'UA': '+380', 'GB': '+44', 'VA': '+39',
        
        # North America
        'AG': '+1', 'BS': '+1', 'BB': '+1', 'BZ': '+501', 'CA': '+1', 'CR': '+506',
        'CU': '+53', 'DM': '+1', 'DO': '+1', 'SV': '+503', 'GD': '+1', 'GT': '+502',
        'HT': '+509', 'HN': '+504', 'JM': '+1', 'MX': '+52', 'NI': '+505', 'PA': '+507',
        'KN': '+1', 'LC': '+1', 'VC': '+1', 'TT': '+1', 'US': '+1',
        
        # Oceania
        'AU': '+61', 'FJ': '+679', 'KI': '+686', 'MH': '+692', 'FM': '+691', 'NR': '+674',
        'NZ': '+64', 'PW': '+680', 'PG': '+675', 'WS': '+685', 'SB': '+677', 'TO': '+676',
        'TV': '+688', 'VU': '+678',
        
        # South America
        'AR': '+54', 'BO': '+591', 'BR': '+55', 'CL': '+56', 'CO': '+57', 'EC': '+593',
        'GY': '+592', 'PY': '+595', 'PE': '+51', 'SR': '+597', 'UY': '+598', 'VE': '+58',
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
    
    # Individual Address Components for Primary Address
    address = models.CharField(max_length=500, blank=True, help_text="Street address")
    city = models.CharField(max_length=100, blank=True, help_text="City")
    state_province = models.CharField(max_length=100, blank=True, help_text="State or Province")
    postal_code = models.CharField(max_length=20, blank=True, help_text="Postal/ZIP code")
    
    # Learning preferences
    preferred_learning_format = models.CharField(max_length=50, blank=True)
    interests = models.TextField(blank=True, help_text="Comma-separated interests")
    
    # Additional Professional Information
    education_level = models.CharField(max_length=100, blank=True, help_text="Highest education level")
    profession = models.CharField(max_length=100, blank=True, help_text="Current profession/occupation")
    years_of_experience = models.PositiveIntegerField(blank=True, null=True, help_text="Years of professional experience")
    
    # Communication Preferences
    COMMUNICATION_PREFERENCES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('whatsapp', 'WhatsApp'),
        ('wechat', 'WeChat'),
        ('sms', 'SMS'),
    ]
    preferred_communication_method = models.CharField(
        max_length=20, 
        choices=COMMUNICATION_PREFERENCES, 
        default='email',
        help_text="Preferred method of communication"
    )
    
    # Marketing and Privacy Consent
    marketing_consent = models.BooleanField(default=False, help_text="Consent to receive marketing communications")
    data_processing_consent = models.BooleanField(default=True, help_text="Consent to data processing")
    newsletter_subscription = models.BooleanField(default=False, help_text="Subscribe to newsletter")
    
    # Additional Notes
    internal_notes = models.TextField(blank=True, help_text="Internal notes (not visible to customer)")
    special_requirements = models.TextField(blank=True, help_text="Special requirements or accommodations")
    
    # Data Source Tracking
    SOURCE_CHOICES = [
        ('', 'Select Source'),
        # Digital Marketing
        ('website', 'Website'),
        ('google_search', 'Google Search'),
        ('social_media', 'Social Media'),
        ('facebook', 'Facebook'),
        ('linkedin', 'LinkedIn'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter/X'),
        ('youtube', 'YouTube'),
        ('email_marketing', 'Email Marketing'),
        ('google_ads', 'Google Ads'),
        ('facebook_ads', 'Facebook Ads'),
        ('online_ad', 'Online Advertisement'),
        
        # Traditional Marketing
        ('print_ad', 'Print Advertisement'),
        ('radio', 'Radio'),
        ('tv', 'Television'),
        ('billboard', 'Billboard'),
        ('flyer', 'Flyer/Brochure'),
        
        # Referrals & Word of Mouth
        ('referral', 'Referral'),
        ('word_of_mouth', 'Word of Mouth'),
        ('existing_customer', 'Existing Customer'),
        ('partner', 'Partner/Affiliate'),
        ('employee', 'Employee Referral'),
        
        # Events & Outreach
        ('conference', 'Conference/Event'),
        ('workshop', 'Workshop'),
        ('webinar', 'Webinar'),
        ('trade_show', 'Trade Show'),
        ('seminar', 'Seminar'),
        ('cold_call', 'Cold Call'),
        ('cold_email', 'Cold Email'),
        
        # Import Sources
        ('csv_import', 'CSV Import'),
        ('data_migration', 'Data Migration'),
        ('api_import', 'API Import'),
        ('bulk_upload', 'Bulk Upload'),
        
        # Direct Contact
        ('walk_in', 'Walk-in'),
        ('phone_inquiry', 'Phone Inquiry'),
        ('email_inquiry', 'Email Inquiry'),
        ('contact_form', 'Contact Form'),
        
        # Other
        ('other', 'Other'),
        ('unknown', 'Unknown'),
    ]
    
    source = models.CharField(
        max_length=100, 
        choices=SOURCE_CHOICES,
        blank=True, 
        help_text="How customer found us"
    )
    referral_source = models.CharField(max_length=100, blank=True, help_text="Referral source if applicable")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        # Build name with title and designation if available
        name_parts = []
        if self.designation:
            name_parts.append(self.get_designation_display())
        elif self.title:
            name_parts.append(self.title)
        
        if self.preferred_name:
            name_parts.append(self.preferred_name)
        else:
            name_parts.append(self.first_name)
        
        name_parts.append(self.last_name)
        
        if self.name_suffix:
            name_parts.append(self.name_suffix)
        
        full_name = ' '.join(name_parts)
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
    
    def auto_set_country_codes(self, force_update=False):
        """Automatically set country codes based on selected country"""
        country_code = self.get_country_code()
        if country_code:
            # Always update primary phone country code when country changes
            if not self.phone_primary_country_code or force_update:
                if self.phone_primary:
                    self.phone_primary_country_code = country_code
            
            # Only set secondary phone country code if empty (allow user override)
            if not self.phone_secondary_country_code and self.phone_secondary:
                self.phone_secondary_country_code = country_code
            
            # Auto-set WhatsApp and fax if empty
            if not self.whatsapp_country_code and self.whatsapp_number:
                self.whatsapp_country_code = country_code
            if not self.fax_country_code and self.fax:
                self.fax_country_code = country_code
            
            # Auto-set emergency contact if empty
            if not hasattr(self, 'emergency_contact_country_code'):
                # This field doesn't exist yet, will be added in next enhancement
                pass
    
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
    
    # Note: address field is defined above as models.CharField
    # Removed conflicting @property to avoid field/property collision


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

class EmailTemplate(models.Model):
    """Email templates for standardized communications"""
    
    TEMPLATE_TYPES = [
        ('welcome', 'Welcome Email'),
        ('course_reminder', 'Course Reminder'),
        ('enrollment_confirmation', 'Enrollment Confirmation'),
        ('payment_confirmation', 'Payment Confirmation'),
        ('newsletter', 'Newsletter'),
        ('marketing', 'Marketing Email'),
        ('event_invitation', 'Event Invitation'),
        ('follow_up', 'Follow-up Email'),
        ('survey', 'Survey Request'),
        ('birthday', 'Birthday Wishes'),
        ('custom', 'Custom Template'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, help_text="Template name for internal reference")
    template_type = models.CharField(max_length=30, choices=TEMPLATE_TYPES)
    subject = models.CharField(max_length=200, help_text="Email subject line (supports variables)")
    content_text = models.TextField(help_text="Plain text content (supports variables)")
    content_html = models.TextField(blank=True, help_text="HTML content (supports variables)")
    
    # Template variables and personalization
    available_variables = models.TextField(
        blank=True,
        help_text="Available template variables (JSON format): {{first_name}}, {{course_title}}, etc."
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, blank=True, help_text="Who created this template")
    
    # Usage tracking
    usage_count = models.PositiveIntegerField(default=0, help_text="How many times this template has been used")
    last_used = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['template_type', 'status']),
            models.Index(fields=['status', '-updated_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
    
    def increment_usage(self):
        """Increment usage counter and update last_used timestamp"""
        from django.utils import timezone
        self.usage_count += 1
        self.last_used = timezone.now()
        self.save(update_fields=['usage_count', 'last_used'])

class EmailCampaign(models.Model):
    """Email marketing campaigns"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
    ]
    
    TARGET_AUDIENCE_CHOICES = [
        ('all_customers', 'All Customers'),
        ('active_customers', 'Active Customers'),
        ('prospects', 'Prospects'),
        ('students', 'Students'),
        ('corporate_clients', 'Corporate Clients'),
        ('newsletter_subscribers', 'Newsletter Subscribers'),
        ('marketing_consent', 'Marketing Consent Given'),
        ('custom_filter', 'Custom Filter'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Campaign content
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=200)
    content_text = models.TextField()
    content_html = models.TextField(blank=True)
    
    # Targeting
    target_audience = models.CharField(max_length=30, choices=TARGET_AUDIENCE_CHOICES)
    custom_filter = models.JSONField(blank=True, null=True, help_text="Custom filter criteria in JSON format")
    
    # Scheduling
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    # Campaign metrics
    total_recipients = models.PositiveIntegerField(default=0)
    emails_sent = models.PositiveIntegerField(default=0)
    emails_delivered = models.PositiveIntegerField(default=0)
    emails_opened = models.PositiveIntegerField(default=0)
    emails_clicked = models.PositiveIntegerField(default=0)
    emails_bounced = models.PositiveIntegerField(default=0)
    emails_failed = models.PositiveIntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['target_audience', 'status']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"
    
    @property
    def open_rate(self):
        """Calculate email open rate percentage"""
        if self.emails_delivered > 0:
            return round((self.emails_opened / self.emails_delivered) * 100, 2)
        return 0
    
    @property
    def click_rate(self):
        """Calculate email click rate percentage"""
        if self.emails_delivered > 0:
            return round((self.emails_clicked / self.emails_delivered) * 100, 2)
        return 0
    
    @property
    def bounce_rate(self):
        """Calculate email bounce rate percentage"""
        if self.emails_sent > 0:
            return round((self.emails_bounced / self.emails_sent) * 100, 2)
        return 0

class EmailLog(models.Model):
    """Detailed logging for individual email sends"""
    
    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('opened', 'Opened'),
        ('clicked', 'Clicked'),
        ('bounced', 'Bounced'),
        ('failed', 'Failed'),
        ('unsubscribed', 'Unsubscribed'),
        ('complained', 'Spam Complaint'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    campaign = models.ForeignKey(EmailCampaign, on_delete=models.CASCADE, null=True, blank=True)
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Email details
    recipient_email = models.EmailField()
    subject = models.CharField(max_length=200)
    content_text = models.TextField()
    content_html = models.TextField(blank=True)
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued')
    external_message_id = models.CharField(max_length=200, blank=True)
    
    # Timestamps
    queued_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    bounced_at = models.DateTimeField(null=True, blank=True)
    failed_at = models.DateTimeField(null=True, blank=True)
    
    # Error handling
    error_message = models.TextField(blank=True)
    retry_count = models.PositiveIntegerField(default=0)
    max_retries = models.PositiveIntegerField(default=3)
    
    # Analytics
    ip_address = models.GenericIPAddressField(null=True, blank=True, help_text="IP address for opens/clicks")
    user_agent = models.TextField(blank=True, help_text="User agent for opens/clicks")
    
    class Meta:
        ordering = ['-queued_at']
        indexes = [
            models.Index(fields=['customer', '-queued_at']),
            models.Index(fields=['campaign', 'status']),
            models.Index(fields=['status', '-queued_at']),
            models.Index(fields=['recipient_email', '-queued_at']),
        ]
    
    def __str__(self):
        return f"Email to {self.recipient_email} - {self.get_status_display()}"
    
    def update_status(self, new_status, error_message=None, ip_address=None, user_agent=None):
        """Update email status with timestamp"""
        from django.utils import timezone
        
        self.status = new_status
        timestamp = timezone.now()
        
        if new_status == 'sent':
            self.sent_at = timestamp
        elif new_status == 'delivered':
            self.delivered_at = timestamp
        elif new_status == 'opened':
            self.opened_at = timestamp
            if ip_address:
                self.ip_address = ip_address
            if user_agent:
                self.user_agent = user_agent
        elif new_status == 'clicked':
            self.clicked_at = timestamp
            if ip_address:
                self.ip_address = ip_address
            if user_agent:
                self.user_agent = user_agent
        elif new_status == 'bounced':
            self.bounced_at = timestamp
        elif new_status == 'failed':
            self.failed_at = timestamp
        
        if error_message:
            self.error_message = error_message
        
        self.save()

class EmailSubscription(models.Model):
    """Manage email subscriptions and unsubscribes"""
    
    SUBSCRIPTION_TYPES = [
        ('newsletter', 'Newsletter'),
        ('marketing', 'Marketing Emails'),
        ('course_updates', 'Course Updates'),
        ('event_notifications', 'Event Notifications'),
        ('system_notifications', 'System Notifications'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=30, choices=SUBSCRIPTION_TYPES)
    is_subscribed = models.BooleanField(default=True)
    
    # Tracking
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    unsubscribe_reason = models.CharField(max_length=200, blank=True)
    
    # Unsubscribe token for secure unsubscribe links
    unsubscribe_token = models.CharField(max_length=64, unique=True, blank=True)
    
    class Meta:
        unique_together = ['customer', 'subscription_type']
        indexes = [
            models.Index(fields=['customer', 'is_subscribed']),
            models.Index(fields=['subscription_type', 'is_subscribed']),
        ]
    
    def __str__(self):
        status = "Subscribed" if self.is_subscribed else "Unsubscribed"
        return f"{self.customer.email_primary} - {self.get_subscription_type_display()} ({status})"
    
    def save(self, *args, **kwargs):
        if not self.unsubscribe_token:
            import secrets
            self.unsubscribe_token = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)
    
    def unsubscribe(self, reason=None):
        """Unsubscribe user with timestamp and reason"""
        from django.utils import timezone
        self.is_subscribed = False
        self.unsubscribed_at = timezone.now()
        if reason:
            self.unsubscribe_reason = reason
        self.save()