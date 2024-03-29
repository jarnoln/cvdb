"""
Django settings for cvdb project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys
# from django.utils.log import RequireDebugFalse, RequireDebugTrue

SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SETTINGS_DIR)
SITE_DIR = os.path.dirname(BASE_DIR)
PROJECT_NAME = os.path.basename(SETTINGS_DIR)


try:
    from .site_config import ALLOWED_HOSTS
    from .site_config import CORS_ALLOWED_ORIGINS
    from .site_config import CSRF_COOKIE_SECURE
    from .site_config import CSRF_TRUSTED_ORIGINS
    from .site_config import DEBUG
    from .site_config import SECRET_KEY
    from .site_config import SECURE_SSL_REDIRECT
    from .site_config import SESSION_COOKIE_SECURE
except ImportError:
    print("Site configuration file does not exist or not properly configured. How to create it:")
    print("python {}/generate_site_config.py {}/site_config.py".format(PROJECT_NAME, PROJECT_NAME))
    sys.exit(1)

if DEBUG:
    LOG_DIR = BASE_DIR
else:
    LOG_DIR = os.path.join(SITE_DIR, 'log')

assert os.path.exists(LOG_DIR), 'Log directory {} does not exist'.format(LOG_DIR)

# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

SITE_ID = 1
ADMINS = [('Jarno', 'jarnoln@gmail.com')]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'users',
    'viewcv',  # Needs to be defined before allauth to override templates
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'behave_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

ROOT_URLCONF = 'cvdb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'cvdb.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Needed since Django 3.2:
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = []

# Email settings
SERVER_EMAIL = 'django@cvdb.fi'  # Used for error and log messages
DEFAULT_FROM_EMAIL = 'accounts@cvdb.fi'  # Used for normal emails (mostly account email verifications)

# Django allauth settings
# http://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
SOCIALACCOUNT_QUERY_EMAIL = True

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Helsinki'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(SITE_DIR, 'static')

# Security
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = False
X_FRAME_OPTIONS = 'DENY'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            # 'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            # 'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'cvdb.log'),
            'maxBytes': 1024*1024,
            'backupCount': 2,
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'viewcv': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'WARNING',
            'propagate': False
        },
        'django': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'INFO',
        }
    }
}
