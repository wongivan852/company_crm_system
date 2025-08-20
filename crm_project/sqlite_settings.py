# SQLite Development Settings Override
# This forces Django to use SQLite instead of PostgreSQL

from crm_project.settings import *

# Override database to use SQLite with full customer data
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/user/krystal-company-apps/company_crm_system/updated.db',
    }
}

# Development settings with Internet Access
DEBUG = True
SECRET_KEY = 'sqlite-dev-key-not-for-production'
ALLOWED_HOSTS = ['*']  # Allow all hosts for internet access

# Disable HTTPS redirects for development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Static files for development
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

# CORS settings for API access from internet
if 'corsheaders' in [app for app in INSTALLED_APPS if 'corsheaders' in app]:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True

# Security headers for internet access
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Network configuration
USE_TZ = True
TIME_ZONE = 'UTC'

print("✅ Configured for internet access")
