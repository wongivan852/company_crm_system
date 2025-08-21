# Database Configuration - Fixed for Environment Synchronization
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': config('DB_NAME', default='crm_db'),
        'USER': config('DB_USER', default='crm_user'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        # Fix connection issues for large imports
        'CONN_MAX_AGE': config('DB_CONN_MAX_AGE', default=0, cast=int),  # Disable connection pooling for imports
        'CONN_HEALTH_CHECKS': config('DB_CONN_HEALTH_CHECKS', default=True, cast=bool),
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c default_transaction_isolation=read_committed'
        } if config('DB_ENGINE', default='django.db.backends.postgresql').endswith('postgresql') else {},
        # Add timeout settings for large operations
        'TEST': {
            'NAME': config('DB_NAME', default='crm_db') + '_test',
        },
        # Transaction settings for data consistency
        'ATOMIC_REQUESTS': True,  # Wrap each view in a transaction
    }
}

# Add database routing for read/write separation if needed
DATABASE_ROUTERS = []

# Cache configuration for database query optimization
if config('DB_ENGINE', default='django.db.backends.postgresql').endswith('postgresql'):
    # PostgreSQL specific optimizations
    DATABASES['default']['OPTIONS'].update({
        'init_command': 'SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED',
        'charset': 'utf8mb4',
    })
    
# Logging configuration for database debugging
if DEBUG:
    LOGGING['loggers']['django.db.backends'] = {
        'level': 'DEBUG',
        'handlers': ['performance_file', 'console'],
        'propagate': False,
    }

# REST Framework pagination settings - Fix for data display issues
REST_FRAMEWORK['PAGE_SIZE'] = 100  # Increase from 20 to see more records
REST_FRAMEWORK['PAGE_SIZE_QUERY_PARAM'] = 'page_size'
REST_FRAMEWORK['MAX_PAGE_SIZE'] = 1000  # Allow up to 1000 records per page for admin