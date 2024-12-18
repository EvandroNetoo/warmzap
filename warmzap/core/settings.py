import os
import sys
from pathlib import Path

from django.contrib import messages

from core.env_settings import env_settings

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, '../apps'))

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env_settings.SECRET_KEY

DEBUG = env_settings.DEBUG

ALLOWED_HOSTS = env_settings.ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party apps
    'django_htmx',
    'django_cotton',
    'widget_tweaks',
    'django_celery_beat',
    'import_export',
    'channels',
    'corsheaders',
    # Project apps
    'accounts',
    'chip_heater',
    'settings',
    'payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.LoginRequiredMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]


ROOT_URLCONF = 'core.urls'

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
                'core.context_processors.sidebar',
            ],
        },
    },
]

ASGI_APPLICATION = 'core.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.pubsub.RedisPubSubChannelLayer',
        'CONFIG': {
            'hosts': [
                {
                    'address': env_settings.REDIS_URL,
                }
            ]
        },
    }
}


# Database

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env_settings.DB_NAME,
            'USER': env_settings.DB_USER,
            'PASSWORD': env_settings.DB_PASSWORD,
            'HOST': env_settings.DB_HOST,
            'PORT': env_settings.DB_PORT,
        }
    }


# Accounts

AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = ('accounts.backends.CustomBackend',)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]

LOGIN_URL = 'signin'


# Internationalization

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'templates/static']


# Media files

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CSRF

CSRF_TRUSTED_ORIGINS = ['https://warmzap.vps-kinghost.net']


# Cotton

COTTON_DIR = 'components'


# Messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}


# Debug toolbar

INTERNAL_IPS = ['127.0.0.1']


# Celery


CELERY_BROKER_URL = f'{env_settings.REDIS_URL}/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'


# Asaas

ASAAS_ACCESS_TOKEN = env_settings.ASAAS_ACCESS_TOKEN
# if not DEBUG:
#     SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#     SECURE_SSL_REDIRECT = True
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
