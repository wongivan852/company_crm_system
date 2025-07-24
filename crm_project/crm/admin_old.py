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
        }),
        ('Additional Information', {
            'fields': ('address', 'preferred_learning_format', 'interests')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['send_welcome_message', 'mark_as_active', 'mark_as_inactive']
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'
    
    def send_welcome_message(self, request, queryset):
        """Send welcome message to selected customers"""
        comm_manager = CommunicationManager()
        success_count = 0
        
        for customer in queryset:
            success, message = comm_manager.send_welcome_message(customer)
            if success:
                success_count += 1
        
        self.message_user(request, f"Welcome messages sent to {success_count} customers.")
    send_welcome_message.short_description = "Send welcome message"
    
    def mark_as_active(self, request, queryset):
        queryset.update(status='active')
    mark_as_active.short_description = "Mark as active"
    
    def mark_as_inactive(self, request, queryset):
        queryset.update(status='inactive')
    mark_as_inactive.short_description = "Mark as inactive"

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'course_type', 'start_date', 'duration_hours', 
        'price', 'enrolled_count', 'is_active'
    ]
    list_filter = ['course_type', 'is_active', 'start_date']
    search_fields = ['title', 'description']
    readonly_fields = ['id', 'created_at', 'enrolled_count']
    
    fieldsets = (
        ('Course Information', {
            'fields': ('title', 'description', 'course_type', 'duration_hours', 'price')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date', 'registration_deadline')
        }),
        ('Settings', {
            'fields': ('max_participants', 'is_active')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'enrolled_count'),
            'classes': ('collapse',)
        })
    )
    
    def enrolled_count(self, obj):
        count = obj.enrollment_set.filter(status__in=['registered', 'confirmed']).count()
        return f"{count}/{obj.max_participants}"
    enrolled_count.short_description = 'Enrolled'

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = [
        'customer', 'course', 'status', 'payment_status', 'enrollment_date'
    ]
    list_filter = ['status', 'payment_status', 'enrollment_date', 'course']
    search_fields = ['customer__first_name', 'customer__last_name', 'course__title']
    readonly_fields = ['id', 'enrollment_date']
    
    fieldsets = (
        ('Enrollment Information', {
            'fields': ('customer', 'course', 'enrollment_date')
        }),
        ('Status', {
            'fields': ('status', 'payment_status')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('System Information', {
            'fields': ('id',),
            'classes': ('collapse',)
        })
    )
    
    actions = ['send_course_reminder', 'mark_as_confirmed', 'mark_as_completed']
    
    def send_course_reminder(self, request, queryset):
        """Send course reminder to selected enrollments"""
        comm_manager = CommunicationManager()
        success_count = 0
        
        for enrollment in queryset:
            success, message = comm_manager.send_course_reminder(enrollment)
            if success:
                success_count += 1
        
        self.message_user(request, f"Course reminders sent to {success_count} students.")
    send_course_reminder.short_description = "Send course reminder"
    
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_as_confirmed.short_description = "Mark as confirmed"
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Mark as completed"

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'venue', 'start_date', 'end_date', 
        'registration_fee', 'registered_count', 'is_active'
    ]
    list_filter = ['is_active', 'start_date']
    search_fields = ['name', 'description', 'venue']
    readonly_fields = ['id', 'created_at', 'registered_count']
    
    fieldsets = (
        ('Conference Information', {
            'fields': ('name', 'description', 'venue')
        }),
        ('Schedule & Pricing', {
            'fields': ('start_date', 'end_date', 'registration_fee')
        }),
        ('Settings', {
            'fields': ('max_attendees', 'is_active')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'registered_count'),
            'classes': ('collapse',)
        })
    )
    
    def registered_count(self, obj):
        count = obj.conferenceregistration_set.count()
        return f"{count}/{obj.max_attendees}"
    registered_count.short_description = 'Registered'

@admin.register(ConferenceRegistration)
class ConferenceRegistrationAdmin(admin.ModelAdmin):
    list_display = ['customer', 'conference', 'registration_date']
    list_filter = ['conference', 'registration_date']
    search_fields = ['customer__first_name', 'customer__last_name', 'conference__name']
    readonly_fields = ['id', 'registration_date']

@admin.register(CommunicationLog)
class CommunicationLogAdmin(admin.ModelAdmin):
    list_display = [
        'customer', 'channel', 'subject', 'is_outbound', 'sent_at'
    ]
    list_filter = ['channel', 'is_outbound', 'sent_at']
    search_fields = ['customer__first_name', 'customer__last_name', 'subject', 'content']
    readonly_fields = ['id', 'sent_at', 'external_message_id']
    
    fieldsets = (
        ('Communication Details', {
            'fields': ('customer', 'channel', 'subject', 'content')
        }),
        ('Metadata', {
            'fields': ('is_outbound', 'sent_at', 'external_message_id'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('id',),
            'classes': ('collapse',)
        })
    )
    
    def has_add_permission(self, request):
        return False  # Communication logs are created automatically
    
    def has_change_permission(self, request, obj=None):
        return False  # Communication logs should not be edited