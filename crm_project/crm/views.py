# views.py
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .models import Customer, Course, Enrollment, Conference, ConferenceRegistration, CommunicationLog
from .serializers import (
    CustomerSerializer, CourseSerializer, EnrollmentSerializer, 
    ConferenceSerializer, CommunicationLogSerializer
)
from .communication_services import CommunicationManager

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['customer_type', 'status', 'preferred_communication']
    search_fields = ['first_name', 'last_name', 'email', 'company']
    ordering_fields = ['created_at', 'last_name', 'first_name']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Send message to customer via their preferred channel"""
        customer = self.get_object()
        channel = request.data.get('channel', customer.preferred_communication)
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
            Q(email__icontains=contact) |
            Q(phone__icontains=contact) |
            Q(whatsapp_number__icontains=contact)
        )
        
        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data)

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
