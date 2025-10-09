from os import environ, urandom
from pathlib import Path

from dotenv import load_dotenv

from .base import *

load_dotenv()

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

SECRET_KEY: str = environ.get('DJANGO_SECRET_KEY', urandom(32).hex())
DEBUG: bool = environ.get('DJANGO_DEBUG', 'True') == 'True'
ALLOWED_HOSTS: list[str] = environ.get(
    'DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# applications
INSTALLED_APPS: list[str] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party
    'rest_framework',
    'rest_framework.authtoken',
    # local apps
    'events.apps.EventsConfig',
]

MIDDLEWARE: list[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES: list[dict] = [
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

WSGI_APPLICATION = 'config.wsgi.application'

# SQLite db for development
DATABASES: dict[str, dict[str, str]] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE: str = 'en-us'
TIME_ZONE: str = 'UTC'
USE_I18N: bool = True
USE_TZ: bool = True

# static files
STATIC_URL: str = '/static/'
STATICFILES_DIRS: list[Path] = [BASE_DIR / 'static']
STATIC_ROOT: Path = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'

# custom user model
AUTH_USER_MODEL: str = environ.get('AUTH_USER_MODEL', 'auth.User')

# development email backend
EMAIL_BACKEND: str = environ.get(
    'EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')

# redirect users to home after login/logout when no "next" provided
LOGIN_REDIRECT_URL: str = 'events:event-list'
LOGOUT_REDIRECT_URL: str = 'events:home'

if DEBUG:
    try:
        INSTALLED_APPS: list[str] = list(dict.fromkeys(INSTALLED_APPS))
    except Exception:
        # keep original list
        pass

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
