# forms.py - Django forms for customer management
from django import forms
from .models import Customer, Enrollment, Course, CustomerCommunicationPreference

class CustomerForm(forms.ModelForm):
    """Form for creating and editing customers with enhanced name fields and country selection"""
    
    class Meta:
        model = Customer
        fields = [
            # Enhanced name fields
            'first_name', 'middle_name', 'last_name', 'preferred_name', 'name_suffix',
            
            # Contact information
            'email_primary', 'email_secondary',
            'phone_primary', 'phone_primary_country_code',
            'phone_secondary', 'phone_secondary_country_code', 
            'fax', 'fax_country_code',
            'whatsapp_number', 'whatsapp_country_code',
            'wechat_id',
            
            # Geographic
            'country_region',
            
            # Professional
            'company_primary', 'position_primary', 'company_secondary', 'position_secondary',
            'company_website', 'address_primary', 'address_secondary',
            
            # Social media
            'linkedin_profile', 'facebook_profile', 'twitter_handle', 'instagram_handle',
            
            # CRM fields
            'customer_type', 'status', 'preferred_learning_format', 'interests', 'marketing_consent'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name (required)'
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter middle name(s) (optional)'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name (required)'
            }),
            'preferred_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nickname or preferred name (optional)'
            }),
            'name_suffix': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Jr., Sr., III, etc. (optional)'
            }),
            'email_primary': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter primary email address'
            }),
            'email_secondary': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter secondary email address (optional)'
            }),
            'phone_primary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number (without country code)'
            }),
            'phone_primary_country_code': forms.TextInput(attrs={
                'class': 'form-control country-code',
                'placeholder': '+1',
                'readonly': True
            }),
            'phone_secondary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter secondary phone number (without country code)'
            }),
            'phone_secondary_country_code': forms.TextInput(attrs={
                'class': 'form-control country-code',
                'placeholder': '+1',
                'readonly': True
            }),
            'fax': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter fax number (without country code)'
            }),
            'fax_country_code': forms.TextInput(attrs={
                'class': 'form-control country-code',
                'placeholder': '+1',
                'readonly': True
            }),
            'whatsapp_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter WhatsApp number (without country code)'
            }),
            'whatsapp_country_code': forms.TextInput(attrs={
                'class': 'form-control country-code',
                'placeholder': '+1',
                'readonly': True
            }),
            'country_region': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_country_region',
                'onchange': 'updateCountryCodes(this.value)'
            }),
            'wechat_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter WeChat ID'
            }),
            'customer_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'company_primary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter primary company'
            }),
            'position_primary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter primary position'
            }),
            'company_secondary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter secondary company (optional)'
            }),
            'position_secondary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter secondary position (optional)'
            }),
            'company_website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company website URL'
            }),
            'address_primary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter primary address'
            }),
            'address_secondary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter secondary address (optional)'
            }),
            'country_region': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter country/region'
            }),
            'linkedin_profile': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter LinkedIn profile URL'
            }),
            'facebook_profile': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Facebook profile URL'
            }),
            'twitter_handle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Twitter/X handle (without @)'
            }),
            'instagram_handle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Instagram handle (without @)'
            }),
            'preferred_learning_format': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Online, In-person, Hybrid'
            }),
            'interests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter interests (comma-separated)'
            }),
            'marketing_consent': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class CustomerCommunicationPreferenceForm(forms.ModelForm):
    """Form for managing customer communication preferences"""
    
    class Meta:
        model = CustomerCommunicationPreference
        fields = ['communication_type', 'priority', 'is_active', 'notes']
        widgets = {
            'communication_type': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
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
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
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
        widget=forms.Select(attrs={'class': 'form-control'})
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
        widget=forms.Select(attrs={'class': 'form-control'})
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
