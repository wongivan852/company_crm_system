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

# Development settings
DEBUG = True
SECRET_KEY = 'sqlite-dev-key-not-for-production'
ALLOWED_HOSTS = ['*']

# Disable HTTPS redirects
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Static files for development
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

print("✅ Using SQLite database settings")
