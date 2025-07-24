# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Customer, Course, Enrollment, Conference, ConferenceRegistration, CommunicationLog, CustomerCommunicationPreference
from .communication_services import CommunicationManager

class CustomerCommunicationPreferenceInline(admin.TabularInline):
    model = CustomerCommunicationPreference
    extra = 1
    fields = ['communication_type', 'priority', 'is_active', 'notes']
    ordering = ['priority', 'communication_type']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'email_primary', 'customer_type', 'status', 
        'country_region', 'marketing_consent', 'created_at'
    ]
    list_filter = [
        'customer_type', 'status', 'country_region',
        'marketing_consent', 'created_at'
    ]
    search_fields = [
        'first_name', 'last_name', 'email_primary', 'email_secondary',
        'company_primary', 'company_secondary', 'phone_primary', 'phone_secondary'
    ]
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [CustomerCommunicationPreferenceInline]
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'country_region')
        }),
        ('Email Addresses', {
            'fields': ('email_primary', 'email_secondary')
        }),
        ('Phone Numbers', {
            'fields': ('phone_primary', 'phone_secondary', 'fax')
        }),
        ('Messaging Apps', {
            'fields': ('whatsapp_number', 'wechat_id')
        }),
        ('Social Media', {
            'fields': ('linkedin_profile', 'facebook_profile', 'twitter_handle', 'instagram_handle'),
            'classes': ('collapse',)
        }),
        ('Professional Information', {
            'fields': (
                'customer_type', 'status',
                'company_primary', 'position_primary',
                'company_secondary', 'position_secondary',
                'company_website'
            )
        }),
        ('Addresses', {
            'fields': ('address_primary', 'address_secondary'),
            'classes': ('collapse',)
        }),
        ('Learning Preferences', {
            'fields': ('preferred_learning_format', 'interests', 'marketing_consent')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'

    actions = ['send_welcome_email', 'export_to_csv']
    
    def send_welcome_email(self, request, queryset):
        comm_manager = CommunicationManager()
        success_count = 0
        
        for customer in queryset:
            if customer.email_primary and customer.marketing_consent:
                success, message = comm_manager.send_welcome_message(customer)
                if success:
                    success_count += 1
        
        self.message_user(request, f'Welcome emails sent to {success_count} customers.')
    send_welcome_email.short_description = "Send welcome email to selected customers"

@admin.register(CustomerCommunicationPreference)
class CustomerCommunicationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['customer', 'communication_type', 'priority', 'is_active', 'created_at']
    list_filter = ['communication_type', 'priority', 'is_active']
    search_fields = ['customer__first_name', 'customer__last_name', 'customer__email_primary']
    readonly_fields = ['id', 'created_at', 'updated_at']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'course_type', 'start_date', 'duration_hours', 'price', 'max_participants', 'is_active']
    list_filter = ['course_type', 'is_active', 'start_date']
    search_fields = ['title', 'description']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'start_date'

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'course', 'status', 'payment_status', 'enrollment_date']
    list_filter = ['status', 'payment_status', 'enrollment_date']
    search_fields = ['customer__first_name', 'customer__last_name', 'course__title']
    readonly_fields = ['id']
    date_hierarchy = 'enrollment_date'

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ['name', 'venue', 'start_date', 'end_date', 'registration_fee', 'max_attendees', 'is_active']
    list_filter = ['is_active', 'start_date']
    search_fields = ['name', 'description', 'venue']
    readonly_fields = ['id', 'created_at']
    date_hierarchy = 'start_date'

@admin.register(ConferenceRegistration)
class ConferenceRegistrationAdmin(admin.ModelAdmin):
    list_display = ['customer', 'conference', 'registration_date']
    list_filter = ['registration_date']
    search_fields = ['customer__first_name', 'customer__last_name', 'conference__name']
    readonly_fields = ['id']
    date_hierarchy = 'registration_date'

@admin.register(CommunicationLog)
class CommunicationLogAdmin(admin.ModelAdmin):
    list_display = ['customer', 'channel', 'subject', 'sent_at', 'is_outbound']
    list_filter = ['channel', 'is_outbound', 'sent_at']
    search_fields = ['customer__first_name', 'customer__last_name', 'subject', 'content']
    readonly_fields = ['id', 'sent_at']
    date_hierarchy = 'sent_at'
    
    def has_add_permission(self, request):
        return False  # Prevent manual creation of communication logs
