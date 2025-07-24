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
    # Web Interface Routes
    path('', frontend_views.dashboard, name='dashboard'),
    path('customers/', frontend_views.customer_list, name='customer_list'),
    path('customers/create/', frontend_views.customer_create, name='customer_create'),
    path('customers/<uuid:customer_id>/', frontend_views.customer_detail, name='customer_detail'),
    path('customers/<uuid:customer_id>/edit/', frontend_views.customer_edit, name='customer_edit'),
    path('customers/<uuid:customer_id>/delete/', frontend_views.customer_delete, name='customer_delete'),
    path('customers/<uuid:customer_id>/message/', frontend_views.send_message, name='send_message'),
    
    # API Routes
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
