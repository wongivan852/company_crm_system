# frontend_views.py - Web interface for customer management
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from .models import Customer, Course, Enrollment, Conference
from .forms import CustomerForm, EnrollmentForm
from .communication_services import CommunicationManager
from .tasks import send_welcome_message_task
from .utils import generate_customer_csv_response

@login_required
def dashboard(request):
    """CRM Dashboard with key metrics - SECURE LOGIN REQUIRED"""
    # Key metrics
    total_customers = Customer.objects.count()
    active_customers = Customer.objects.filter(status='active').count()
    total_courses = Course.objects.filter(is_active=True).count() if hasattr(Course, 'objects') else 0
    total_enrollments = Enrollment.objects.filter(status__in=['registered', 'confirmed']).count() if hasattr(Enrollment, 'objects') else 0
    
    # Recent customers
    recent_customers = Customer.objects.order_by('-created_at')[:5]
    
    # Upcoming courses
    from django.utils import timezone
    upcoming_courses = Course.objects.filter(
        start_date__gte=timezone.now(),
        is_active=True
    ).order_by('start_date')[:5] if hasattr(Course, 'start_date') else []
    
    context = {
        'total_customers': total_customers,
        'active_customers': active_customers,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'recent_customers': recent_customers,
        'upcoming_courses': upcoming_courses,
        'page_title': 'Dashboard - Secure Access',
    }
    return render(request, 'crm/dashboard.html', context)

@login_required
def customer_create(request):
    """Create new customer - SECURE LOGIN REQUIRED"""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'Customer {customer.first_name} {customer.last_name} created successfully!')
            return redirect('crm:customer_list')
    else:
        form = CustomerForm()
    
    context = {
        'form': form, 
        'title': 'Add New Customer - Secure Access',
        'page_title': 'Add Customer - Secure Access'
    }
    return render(request, 'crm/customer_form.html', context)

@login_required
def export_customers_csv(request):
    """Export customer data to CSV - SECURE LOGIN REQUIRED"""
    return generate_customer_csv_response()

@login_required
@login_required
def customer_list(request):
    """List all customers with search and filter capabilities - SECURE LOGIN REQUIRED"""
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
    
    # Filter by customer type
    customer_type = request.GET.get('customer_type')
    if customer_type:
        customers = customers.filter(customer_type=customer_type)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        customers = customers.filter(status=status)
    
    # Pagination
    paginator = Paginator(customers, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'customers': page_obj,  # For backward compatibility
        'search_query': search_query,
        'customer_types': Customer.CUSTOMER_TYPES,
        'statuses': Customer.STATUS_CHOICES,
        'selected_type': customer_type,
        'selected_status': status,
        'page_title': 'Customer List - Secure Access',
    }
    return render(request, 'crm/customer_list.html', context)

@login_required
def customer_detail(request, customer_id):
    """View customer details with communication history"""
    customer = get_object_or_404(Customer, id=customer_id)
    enrollments = Enrollment.objects.filter(customer=customer).select_related('course')
    communications = customer.communicationlog_set.all().order_by('-sent_at')[:10]
    
    context = {
        'customer': customer,
        'enrollments': enrollments,
        'communications': communications,
    }
    return render(request, 'crm/customer_detail.html', context)

@login_required
def customer_create(request):
    """Create new customer"""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            
            # Send welcome message asynchronously
            send_welcome_message_task.delay(str(customer.id))
            
            messages.success(request, f'Customer {customer.first_name} {customer.last_name} created successfully!')
            return redirect('crm:customer_detail', customer_id=customer.id)
    else:
        form = CustomerForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'crm/customer_form.html', context)

@login_required
def customer_edit(request, customer_id):
    """Edit existing customer"""
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Customer {customer.first_name} {customer.last_name} updated successfully!')
            return redirect('crm:customer_detail', customer_id=customer.id)
    else:
        form = CustomerForm(instance=customer)
    
    context = {'form': form, 'customer': customer, 'action': 'Edit'}
    return render(request, 'crm/customer_form.html', context)

@login_required
def customer_delete(request, customer_id):
    """Delete customer"""
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        customer_name = f"{customer.first_name} {customer.last_name}"
        customer.delete()
        messages.success(request, f'Customer {customer_name} deleted successfully!')
        return redirect('crm:customer_list')
    
    context = {'customer': customer}
    return render(request, 'crm/customer_confirm_delete.html', context)

@login_required
def send_message(request, customer_id):
    """Send message to customer"""
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        channel = request.POST.get('channel', customer.preferred_communication)
        subject = request.POST.get('subject', '')
        content = request.POST.get('content', '')
        
        comm_manager = CommunicationManager()
        success, message = comm_manager.send_message(customer, channel, subject, content)
        
        if success:
            messages.success(request, f'Message sent successfully via {channel}!')
        else:
            messages.error(request, f'Failed to send message: {message}')
        
        return redirect('crm:customer_detail', customer_id=customer.id)
    
    context = {
        'customer': customer,
        'channels': [
            ('email', 'Email'),
            ('whatsapp', 'WhatsApp'),
            ('wechat', 'WeChat'),
        ]
    }
    return render(request, 'crm/send_message.html', context)

@login_required
def dashboard_old(request):
    """CRM Dashboard with key metrics"""
    # Key metrics
    total_customers = Customer.objects.count()
    active_customers = Customer.objects.filter(status='active').count()
    total_courses = Course.objects.filter(is_active=True).count()
    total_enrollments = Enrollment.objects.filter(status__in=['registered', 'confirmed']).count()
    
    # Recent customers
    recent_customers = Customer.objects.order_by('-created_at')[:5]
    
    # Upcoming courses
    from django.utils import timezone
    upcoming_courses = Course.objects.filter(
        start_date__gte=timezone.now(),
        is_active=True
    ).order_by('start_date')[:5]
    
    context = {
        'total_customers': total_customers,
        'active_customers': active_customers,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'recent_customers': recent_customers,
        'upcoming_courses': upcoming_courses,
    }
    return render(request, 'crm/dashboard.html', context)

def test_country_code_form(request):
    """Simple test view for country code functionality - NO LOGIN REQUIRED"""
    form = CustomerForm()
    return render(request, 'crm/test_country_code_form.html', {'form': form})
