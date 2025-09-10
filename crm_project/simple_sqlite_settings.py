# Simple SQLite Settings without Custom Middleware
# This should resolve the WSGIRequest object has no attribute 'user' error

from crm_project.settings import *

# Override database to use SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/user/krystal-company-apps/company_crm_system/updated.db',
    }
}

# Basic development settings
DEBUG = True
SECRET_KEY = 'sqlite-dev-key-simple-not-for-production'
ALLOWED_HOSTS = ['*']

# Simplified middleware - remove custom middleware that might cause issues
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Debug toolbar (already included in base settings)
INTERNAL_IPS = ['127.0.0.1', 'localhost']

# Disable HTTPS redirects for development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

print("✅ Simple SQLite configuration loaded (no custom middleware)")
