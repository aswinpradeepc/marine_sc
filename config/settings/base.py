"""
base.py
Base Settings for Django Project
"""

import os

from pathlib import Path

import environ

env = environ.Env()

environ.Env.read_env('.env')

APPLICATION_NAME = 'Django Project'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY", default="django-insecure-cag@!muz(kv)t31hxk6w3b)^vzt62_n1wo8&@89)ueefs6p4-7")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

# Admin URL for the project
ADMIN_URL = env.str("ADMIN_URL", default="admin/")

USE_REDIS = env.bool("USE_REDIS", default=False)
# Allowed hosts
ALLOWED_HOSTS = ['*']

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
]

# CORS settings
CORS_ORIGIN_WHITELIST = [
    "http://localhost:8000",
]

CORS_ORIGIN_ALLOW_ALL = False

# Google API client ID and secret
GOOGLE_CLIENT_ID = env.str("GOOGLE_CLIENT_ID", default="")
GOOGLE_CLIENT_SECRET = env.str("GOOGLE_CLIENT_SECRET", default="")

# Email settings
EMAIL_HOST = env.str("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# Installed apps
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
]

# Third-party apps
THIRD_PARTY_APPS = [
    "rest_framework",
    'drf_yasg',
    'rest_framework_simplejwt',
    'django_filters',
]

# Custom apps
CUSTOM_APPS = [
    'base',
    'authentication',
    'maricon',
    'payment'

]

INSTALLED_APPS += CUSTOM_APPS + THIRD_PARTY_APPS
ASGI_APPLICATION = "config.asgi.application"
# Application name



# Login URL
LOGIN_URL = "/authentication/login/"

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

# Root URL configuration
ROOT_URLCONF = 'config.urls'

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = "authentication.User"

if USE_REDIS:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env.str("REDIS_URL", default="redis://redis:6379/1"),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient"
            },
            "KEY_PREFIX": "kwa_cache"
        }
    }

DATA_UPLOAD_MAX_NUMBER_FIELDS = 3000

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # or appropriate port
EMAIL_HOST_USER = 'eoccusat@gmail.com'
EMAIL_HOST_PASSWORD = 'qsqtmdpbwqfuctip'
EMAIL_USE_TLS = True  # or False depending on your server

