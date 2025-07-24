# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, frontend_views

# API Routes
router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'enrollments', views.EnrollmentViewSet)
router.register(r'conferences', views.ConferenceViewSet)
router.register(r'communications', views.CommunicationLogViewSet)

app_name = 'crm'

urlpatterns = [
    # Public UAT Testing Routes (no login required)
    path('', views.customer_dashboard, name='dashboard'),
    path('customers/', views.public_customer_list, name='customer_list'),
    path('customers/create/', views.public_customer_create, name='customer_create'),
    path('customers/export/csv/', views.export_customers_csv, name='export_customers_csv'),
    
    # Protected Frontend Routes (require login)
    path('secure/', frontend_views.dashboard, name='secure_dashboard'),
    path('secure/customers/', frontend_views.customer_list, name='secure_customer_list'),
    path('secure/customers/create/', frontend_views.customer_create, name='secure_customer_create'),
    path('secure/customers/<uuid:customer_id>/', frontend_views.customer_detail, name='customer_detail'),
    path('secure/customers/<uuid:customer_id>/edit/', frontend_views.customer_edit, name='customer_edit'),
    path('secure/customers/<uuid:customer_id>/delete/', frontend_views.customer_delete, name='customer_delete'),
    path('secure/customers/<uuid:customer_id>/message/', frontend_views.send_message, name='send_message'),
    
    # Additional views
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    
    # API Routes
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
