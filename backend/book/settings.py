"""
Django settings for book project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import multiprocessing
import os
import sys
from pathlib import Path

from django.contrib.messages import constants as messages

import birdseye
import dj_database_url

from core.utils import site_packages
from main.simple_settings import *

BASE_DIR = Path(__file__).parent.parent

ALLOWED_HOSTS = [
    os.environ.get('HEROKU_APP_NAME', '') + '.herokuapp.com',
    'futurecoder.io',
    'localhost',
    '127.0.0.1',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'main',
    'sass_processor',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'django_user_agents',
    'crispy_forms',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'book.middleware.DomainRedirectMiddleware',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = not (Root.DEBUG or Root.DISABLE_HTTPS)

ROOT_URLCONF = 'book.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'book.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default="sqlite:///db.sqlite3")
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static_backend/"
STATICFILES_DIRS = [
    ("birdseye", str(site_packages + "birdseye/static")),
    str(BASE_DIR.parent / f"frontend/build/static")
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]


def WHITENOISE_ADD_HEADERS_FUNCTION(headers, path, url):
    headers["Cross-Origin-Opener-Policy"] = "same-origin"
    headers["Cross-Origin-Embedder-Policy"] = "require-corp"


SASS_PROCESSOR_INCLUDE_FILE_PATTERN = r"^.+\.scss$"
STATIC_ROOT = "static/"
SASS_PROCESSOR_ROOT = STATIC_ROOT

AUTH_USER_MODEL = 'main.User'
LOGIN_REDIRECT_URL = '/toc/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'none'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'APP': {
            'client_id': GITHUB_APP.ID,
            'secret': GITHUB_APP.SECRET,
        }
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'offline',
        }
    },
    'facebook': {
        'METHOD': 'js_sdk',
        'SCOPE': ['email'],
        'APP': {
            'client_id': FACEBOOK_APP.ID,
            'secret': FACEBOOK_APP.SECRET,
        },
    },
}

try:
    multiprocessing.set_start_method("spawn")
except RuntimeError:
    # noinspection PyArgumentList
    assert multiprocessing.get_start_method() == "spawn"
