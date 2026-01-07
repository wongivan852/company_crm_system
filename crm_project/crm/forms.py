# forms.py - Django forms for customer management
from django import forms
from .models import Customer, Enrollment, Course, CustomerCommunicationPreference


class CustomerForm(forms.ModelForm):
    """Enhanced form for creating and editing customers with ALL available fields organized in tabs"""

    class Meta:
        model = Customer
        fields = [
            # Tab 1: Basic Information
            'first_name', 'middle_name', 'last_name', 'preferred_name', 'name_suffix',
            'title', 'designation', 'maiden_name', 'other_names',
            'gender', 'date_of_birth', 'nationality',

            # Tab 1: Emergency Contact
            'emergency_contact_name', 'emergency_contact_relationship',
            'emergency_contact_phone', 'emergency_contact_email',

            # Tab 2: Contact Information
            'email_primary', 'email_secondary',
            'phone_primary', 'phone_primary_country_code',
            'phone_secondary', 'phone_secondary_country_code',
            'fax', 'fax_country_code',
            'whatsapp_number', 'whatsapp_country_code',
            'wechat_id',

            # Tab 2: Social Media
            'linkedin_profile', 'facebook_profile', 'twitter_handle',
            'instagram_handle', 'youtube_handle', 'youtube_channel_url',

            # Tab 3: Professional Information
            'company_primary', 'position_primary',
            'company_secondary', 'position_secondary',
            'company_website',
            'education_level', 'profession', 'years_of_experience',

            # Tab 3: Address
            'country_region',
            'address_primary', 'address_secondary',
            'address', 'city', 'state_province', 'postal_code',

            # Tab 4: Preferences & Consent
            'customer_type', 'status',
            'preferred_communication_method',
            'preferred_learning_format', 'interests',
            'marketing_consent', 'data_processing_consent', 'newsletter_subscription',

            # Tab 5: Internal & Tracking
            'source', 'referral_source',
            'internal_notes', 'special_requirements',
        ]

        widgets = {
            # Basic Information
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter middle name(s)'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'preferred_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nickname or preferred name'
            }),
            'name_suffix': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Jr., Sr., III, etc.'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dr., Prof., Mr., Ms., etc.'
            }),
            'designation': forms.Select(attrs={
                'class': 'form-select'
            }),
            'maiden_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Maiden name (if applicable)'
            }),
            'other_names': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Other names, aliases, or previous names'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'nationality': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter nationality'
            }),

            # Emergency Contact
            'emergency_contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Emergency contact full name'
            }),
            'emergency_contact_relationship': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Spouse, Parent, Sibling'
            }),
            'emergency_contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Emergency contact phone number'
            }),
            'emergency_contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Emergency contact email'
            }),

            # Contact Information
            'email_primary': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Primary email address'
            }),
            'email_secondary': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Secondary email address'
            }),
            'phone_primary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number (without country code)'
            }),
            'phone_primary_country_code': forms.TextInput(attrs={
                'class': 'form-control country-code',
                'placeholder': '+1',
                'style': 'max-width: 80px;'
            }),
            'phone_secondary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Secondary phone number'
            }),
            'phone_secondary_country_code': forms.TextInput(attrs={
                'class': 'form-control country-code',
                'placeholder': '+1',
                'style': 'max-width: 80px;'
            }),
            'fax': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fax number'
            }),
            'fax_country_code': forms.TextInput(attrs={
                'class': 'form-control country-code',
                'placeholder': '+1',
                'style': 'max-width: 80px;'
            }),
            'whatsapp_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'WhatsApp number'
            }),
            'whatsapp_country_code': forms.TextInput(attrs={
                'class': 'form-control country-code',
                'placeholder': '+1',
                'style': 'max-width: 80px;'
            }),
            'wechat_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'WeChat ID'
            }),

            # Social Media
            'linkedin_profile': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.linkedin.com/in/username'
            }),
            'facebook_profile': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.facebook.com/username'
            }),
            'twitter_handle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Twitter/X handle (without @)'
            }),
            'instagram_handle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Instagram handle (without @)'
            }),
            'youtube_handle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'YouTube handle (without @)'
            }),
            'youtube_channel_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://youtube.com/@username'
            }),

            # Professional Information
            'company_primary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Current/Primary company'
            }),
            'position_primary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Current/Primary position'
            }),
            'company_secondary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Secondary/Previous company'
            }),
            'position_secondary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Secondary/Previous position'
            }),
            'company_website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.company.com'
            }),
            'education_level': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Bachelor\'s, Master\'s, PhD'
            }),
            'profession': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Current profession/occupation'
            }),
            'years_of_experience': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Years of experience',
                'min': 0
            }),

            # Address
            'country_region': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_country_region',
                'onchange': 'updateCountryCodes(this.value)'
            }),
            'address_primary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Primary address (Home/Office)'
            }),
            'address_secondary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Secondary address (Mailing/Alternative)'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state_province': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State or Province'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Postal/ZIP code'
            }),

            # Preferences & Consent
            'customer_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'preferred_communication_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            'preferred_learning_format': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Online, In-person, Hybrid'
            }),
            'interests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter interests (comma-separated)'
            }),
            'marketing_consent': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'data_processing_consent': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'newsletter_subscription': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),

            # Internal & Tracking
            'source': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'How did they find us?'
            }),
            'referral_source': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Referral source (if applicable)'
            }),
            'internal_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Internal notes (not visible to customer)'
            }),
            'special_requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Special requirements or accommodations'
            }),
        }

        help_texts = {
            'preferred_name': 'The name this person prefers to be called.',
            'designation': 'Professional or academic designation.',
            'linkedin_profile': 'LinkedIn profile URL or username.',
            'facebook_profile': 'Facebook profile URL or username.',
            'twitter_handle': 'Twitter/X handle without the @ symbol.',
            'instagram_handle': 'Instagram handle without the @ symbol.',
            'youtube_handle': 'YouTube handle without the @ symbol.',
            'youtube_channel_url': 'Full YouTube channel URL.',
            'marketing_consent': 'Consent to receive marketing communications.',
            'data_processing_consent': 'Consent to data processing.',
            'newsletter_subscription': 'Subscribe to newsletter.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields with model defaults not required in the form
        # so the model defaults are used when not provided
        fields_with_defaults = [
            'preferred_communication_method',  # default: 'email'
            'customer_type',  # default: 'individual'
            'status',  # default: 'active'
        ]
        for field_name in fields_with_defaults:
            if field_name in self.fields:
                self.fields[field_name].required = False

        # Make key identification fields required even if model allows blanks
        required_fields = ['first_name', 'last_name', 'email_primary']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True


class CustomerCommunicationPreferenceForm(forms.ModelForm):
    """Form for managing customer communication preferences"""

    class Meta:
        model = CustomerCommunicationPreference
        fields = ['communication_type', 'priority', 'is_active', 'notes']
        widgets = {
            'communication_type': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Work hours only, Weekends preferred'
            })
        }


class EnrollmentForm(forms.ModelForm):
    """Form for course enrollment"""

    class Meta:
        model = Enrollment
        fields = ['customer', 'course', 'status', 'payment_status', 'notes']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes about enrollment'
            })
        }


class MessageForm(forms.Form):
    """Form for sending messages to customers"""

    CHANNEL_CHOICES = [
        ('email_primary', 'Primary Email'),
        ('email_secondary', 'Secondary Email'),
        ('whatsapp', 'WhatsApp'),
        ('wechat', 'WeChat'),
    ]

    channel = forms.ChoiceField(
        choices=CHANNEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter message subject'
        })
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Enter your message content'
        })
    )


class BulkMessageForm(forms.Form):
    """Form for sending bulk messages"""

    CHANNEL_CHOICES = [
        ('email_primary', 'Primary Email'),
        ('whatsapp', 'WhatsApp'),
        ('wechat', 'WeChat'),
    ]

    customer_type = forms.MultipleChoiceField(
        choices=Customer.CUSTOMER_TYPES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    status = forms.MultipleChoiceField(
        choices=Customer.STATUS_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    marketing_consent_only = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    channel = forms.ChoiceField(
        choices=CHANNEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter message subject'
        })
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'placeholder': 'Enter your message content'
        })
    )
