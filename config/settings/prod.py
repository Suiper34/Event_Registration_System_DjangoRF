from os import environ, path
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

from .base import *

# production settings


def get_env_value(env_variable: str, default: str | None = None) -> str | None:
    try:
        return environ.get(env_variable, default)

    except KeyError:
        error_msg = f'set the {env_variable} environment variable'
        raise ImproperlyConfigured(error_msg)


BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

DEBUG: bool = False

ALLOWED_HOSTS: list[str] = environ.get('ALLOWED_HOSTS', '').split(',')

# db configuration
DATABASES: dict[str, dict[str, str]] = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_value('DB_NAME'),
        'USER': get_env_value('DB_USER'),
        'PASSWORD': get_env_value('DB_PASSWORD'),
        'HOST': get_env_value('DB_HOST', 'localhost'),
        'PORT': get_env_value('DB_PORT', '5432'),
    }
}

# ensure production uses safe default
AUTH_USER_MODEL: str = environ.get('AUTH_USER_MODEL', 'auth.User')

# static files path
STATIC_URL: str = '/static/'
STATIC_ROOT: str = path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS: list[str] = [path.join(BASE_DIR, 'static'),]

# media files
MEDIA_URL: str = '/media/'
MEDIA_ROOT: str = path.join(BASE_DIR, 'media')

# security settings
SECURE_BROWSER_XSS_FILTER: bool = True
SECURE_CONTENT_TYPE_NOSNIFF: bool = True
SECURE_SSL_REDIRECT: bool = True
SESSION_COOKIE_SECURE: bool = True
CSRF_COOKIE_SECURE: bool = True
SECURE_HSTS_SECONDS: int = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS: bool = True
SECURE_HSTS_PRELOAD: bool = True

# Email settings
EMAIL_BACKEND: str = get_env_value(
    'EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST: str = get_env_value('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT: int = int(get_env_value('EMAIL_PORT', '587'))
EMAIL_USE_TLS: bool = get_env_value('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER: str | None = get_env_value('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD: str | None = get_env_value('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL: str = get_env_value('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
