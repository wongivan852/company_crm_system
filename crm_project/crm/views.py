# views.py
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
import csv
import datetime
from .models import Customer, Course, Enrollment, Conference, ConferenceRegistration, CommunicationLog
from .serializers import (
    CustomerSerializer, CourseSerializer, EnrollmentSerializer, 
    ConferenceSerializer, CommunicationLogSerializer
)
from .communication_services import CommunicationManager
from .forms import CustomerForm
from .utils import generate_customer_csv_response, validate_uat_access

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['customer_type', 'status']
    search_fields = ['first_name', 'last_name', 'email_primary', 'company_primary']
    ordering_fields = ['created_at', 'last_name', 'first_name']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['post'])
    @throttle_classes([UserRateThrottle])
    def send_message(self, request, pk=None):
        """Send message to customer via their preferred channel"""
        customer = self.get_object()
        channel = request.data.get('channel', 'email')  # Default to email
        subject = request.data.get('subject', '')
        content = request.data.get('content', '')
        
        comm_manager = CommunicationManager()
        success, message = comm_manager.send_message(customer, channel, subject, content)
        
        return Response({
            'status': 'success' if success else 'error',
            'message': message,
            'channel': channel
        })
    
    @action(detail=False, methods=['get'])
    def search_by_contact(self, request):
        """Search customers by email, phone, or WhatsApp"""
        contact = request.query_params.get('contact', '')
        if not contact:
            return Response({'error': 'Contact parameter required'}, status=400)
        
        customers = Customer.objects.filter(
            Q(email_primary__icontains=contact) |
            Q(phone_primary__icontains=contact) |
            Q(whatsapp_number__icontains=contact)
        )
        
        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    @throttle_classes([UserRateThrottle])
    def export_csv(self, request):
        """Export customer data to CSV"""
        # Apply any filtering from the viewset
        queryset = self.filter_queryset(self.get_queryset())
        return generate_customer_csv_response(queryset)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['course_type', 'is_active']
    search_fields = ['title', 'description']
    
    @action(detail=True, methods=['post'])
    def enroll_customer(self, request, pk=None):
        """Enroll a customer in this course"""
        course = self.get_object()
        customer_id = request.data.get('customer_id')
        
        try:
            customer = Customer.objects.get(id=customer_id)
            enrollment, created = Enrollment.objects.get_or_create(
                customer=customer,
                course=course,
                defaults={'status': 'registered'}
            )
            
            if created:
                return Response({'status': 'Customer enrolled successfully'})
            else:
                return Response({'status': 'Customer already enrolled'}, status=400)
                
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=404)

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'payment_status', 'customer', 'course']

class ConferenceViewSet(viewsets.ModelViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description', 'venue']

class CommunicationLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CommunicationLog.objects.all()
    serializer_class = CommunicationLogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer', 'channel', 'is_outbound']
    ordering = ['-sent_at']


# Traditional Django views for admin interface
@login_required
def export_customers_csv(request):
    """Export all customer data to CSV - requires authentication"""
    return generate_customer_csv_response()


def test_dashboard(request):
    """Simple dashboard for testing (no security)"""
    from .models import Course, Enrollment
    context = {
        'total_customers': Customer.objects.count(),
        'active_customers': Customer.objects.filter(status='active').count(),
        'recent_customers': Customer.objects.order_by('-created_at')[:5],
        'total_courses': Course.objects.filter(is_active=True).count() if hasattr(Course, 'objects') else 0,
        'total_enrollments': Enrollment.objects.count() if hasattr(Enrollment, 'objects') else 0,
    }
    return render(request, 'crm/dashboard.html', context)


def customer_dashboard(request):
    """Simple dashboard view for UAT testing (SECURED)"""
    # Validate UAT access
    is_valid, error_message = validate_uat_access(request)
    if not is_valid:
        return HttpResponseForbidden(error_message)
    
    from .models import Course, Enrollment
    context = {
        'total_customers': Customer.objects.count(),
        'active_customers': Customer.objects.filter(status='active').count(),
        'recent_customers': Customer.objects.order_by('-created_at')[:5],
        'total_courses': Course.objects.filter(is_active=True).count() if hasattr(Course, 'objects') else 0,
        'total_enrollments': Enrollment.objects.count() if hasattr(Enrollment, 'objects') else 0,
    }
    return render(request, 'crm/dashboard.html', context)


def public_customer_list(request):
    """Public customer list for UAT testing (SECURED)"""
    # Validate UAT access
    is_valid, error_message = validate_uat_access(request)
    if not is_valid:
        return HttpResponseForbidden(error_message)
    
    customers = Customer.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        customers = customers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email_primary__icontains=search_query) |
            Q(company_primary__icontains=search_query)
        )
    
    context = {
        'customers': customers[:50],  # Limit to 50 for UAT
        'search_query': search_query,
        'customer_types': Customer.CUSTOMER_TYPES,
        'statuses': Customer.STATUS_CHOICES,
    }
    return render(request, 'crm/customer_list.html', context)


def public_customer_create(request):
    """Public customer creation for UAT testing (SECURED)"""
    # Validate UAT access
    is_valid, error_message = validate_uat_access(request)
    if not is_valid:
        return HttpResponseForbidden(error_message)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'Customer {customer.first_name} {customer.last_name} created successfully!')
            return redirect('crm:public_customer_list')
    else:
        form = CustomerForm()
    
    return render(request, 'crm/customer_form.html', {'form': form, 'title': 'Add New Customer'})


def test_customer_create(request):
    """Simple customer creation for testing (no security)"""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'Customer {customer.first_name} {customer.last_name} created successfully!')
            return redirect('crm:test_customer_create')
    else:
        form = CustomerForm()
    
    return render(request, 'crm/customer_form.html', {'form': form, 'title': 'Test Add Customer'})


def test_export_csv(request):
    """Test CSV export for development (no security)"""
    return generate_customer_csv_response()