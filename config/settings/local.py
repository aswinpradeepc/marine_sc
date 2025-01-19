"""
local.py
Local Development Settings
"""

from .base import *

DEBUG = True
# Admin URL
ADMIN_URL = "admin/"

# Database settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files URL
STATIC_URL = '/static/'

# Media files URL
MEDIA_URL = '/media/'

# Base URL for media files (e.g., when serving from a different domain)
MEDIA_BASE_URL = "http://localhost:3000"

# Additional directories to search for static files
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings - allow all origins
CORS_ORIGIN_ALLOW_ALL = True

# Additional allowed hosts
ALLOWED_HOSTS += ["*"]

# Additional trusted CSRF origins
CSRF_TRUSTED_ORIGINS += [
    "http://localhost:8000",
]

# Additional CORS origins whitelist
CORS_ORIGIN_WHITELIST += [
    "http://localhost:8000",
]

CACHE_TIMEOUT = 60  # seconds
