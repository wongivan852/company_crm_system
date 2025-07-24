# forms.py - Django forms for customer management
from django import forms
from .models import Customer, Enrollment, Course, CustomerCommunicationPreference

class CustomerForm(forms.ModelForm):
    """Form for creating and editing customers"""
    
    class Meta:
        model = Customer
        fields = [
            'first_name', 'last_name', 'email_primary', 'email_secondary',
            'phone_primary', 'phone_secondary', 'fax',
            'whatsapp_number', 'wechat_id', 'customer_type', 'status',
            'company_primary', 'position_primary', 'company_secondary', 'position_secondary',
            'company_website', 'address_primary', 'address_secondary', 'country_region',
            'linkedin_profile', 'facebook_profile', 'twitter_handle', 'instagram_handle',
            'preferred_learning_format', 'interests', 'marketing_consent'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
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
                'placeholder': 'Enter primary phone number'
            }),
            'phone_secondary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter secondary phone number (optional)'
            }),
            'fax': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter fax number (optional)'
            }),
                'class': 'form-control',
                'placeholder': '+1234567890'
            }),
            'whatsapp_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1234567890'
            }),
            'wechat_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'WeChat ID'
            }),
            'customer_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company name'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job title'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Full address'
            }),
            'preferred_learning_format': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Online, In-person, Hybrid'
            }),
            'interests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Comma-separated interests'
            }),
            'preferred_communication': forms.Select(attrs={'class': 'form-control'}),
            'marketing_consent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_email(self):
        """Validate email uniqueness"""
        email = self.cleaned_data.get('email')
        if email:
            # Check if email exists for other customers (excluding current instance)
            existing = Customer.objects.filter(email=email)
            if self.instance:
                existing = existing.exclude(id=self.instance.id)
            
            if existing.exists():
                raise forms.ValidationError("A customer with this email already exists.")
        
        return email

class EnrollmentForm(forms.ModelForm):
    """Form for enrolling customers in courses"""
    
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
                'placeholder': 'Additional notes'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active courses
        self.fields['course'].queryset = Course.objects.filter(is_active=True)
        
        # Improve display of customer choices
        self.fields['customer'].queryset = Customer.objects.all()
        self.fields['customer'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name} ({obj.email})"

class MessageForm(forms.Form):
    """Form for sending messages to customers"""
    
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('wechat', 'WeChat'),
    ]
    
    channel = forms.ChoiceField(
        choices=CHANNEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    subject = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Message subject (for email)'
        })
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Enter your message here...'
        })
    )

class BulkMessageForm(forms.Form):
    """Form for sending bulk messages"""
    
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('wechat', 'WeChat'),
    ]
    
    customer_filter = forms.ChoiceField(
        choices=[
            ('all', 'All Customers'),
            ('active', 'Active Customers'),
            ('prospects', 'Prospects'),
            ('marketing_consent', 'Marketing Consent Only'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    channel = forms.ChoiceField(
        choices=CHANNEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    subject = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Message subject (for email)'
        })
    )
    
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'placeholder': 'Enter your message here...'
        })
    )
