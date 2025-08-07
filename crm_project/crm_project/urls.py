"""
URL configuration for crm_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.http import JsonResponse, HttpResponse
import sys
import os

def network_test(request):
    """Simple endpoint to test network connectivity"""
    client_ip = request.META.get('HTTP_X_FORWARDED_FOR', 
                               request.META.get('REMOTE_ADDR', 'Unknown'))
    
    response_data = {
        'status': 'success',
        'message': 'CRM System Network Test',
        'server_ip': '192.168.0.104',
        'client_ip': client_ip,
        'port': '8082',
        'method': request.method,
        'timestamp': str(__import__('datetime').datetime.now()),
        'server': 'Django CRM System'
    }
    
    return JsonResponse(response_data, json_dumps_params={'indent': 2})

def network_landing(request):
    """Landing page for network testing"""
    try:
        with open('/home/user/krystal-company-apps/company_crm_system/network_landing.html', 'r') as f:
            html_content = f.read()
        return HttpResponse(html_content, content_type='text/html')
    except FileNotFoundError:
        return HttpResponse('<h1>Network Test Page</h1><p>Landing page file not found</p>', 
                          content_type='text/html')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication URLs - SECURE LOGIN REQUIRED
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        extra_context={'page_title': 'Secure Login - Learning Institute CRM'}
    ), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(
        next_page='/'
    ), name='logout'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change_form.html'
    ), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name='password_change_done'),
    
    # CRM Application
    path('', include('crm.urls')),
    
    # Network test endpoints
    path('network-test/', network_test, name='network_test'),
    path('network-landing/', network_landing, name='network_landing'),
]

# Add debug toolbar URLs for development
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
