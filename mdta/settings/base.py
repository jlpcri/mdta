"""
Django settings for mdta project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TMP_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", 'tmp'))

MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", 'media'))

MEDIA_URL = '/mdta/media/'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# LDAP Settings
import ldap
from django_auth_ldap.config import LDAPSearch
LOGIN_URL = '/mdta/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_auth_ldap.backend.LDAPBackend',
)

AUTH_LDAP_SERVER_URI = "ldap://10.27.116.51"
AUTH_LDAP_BIND_DN = "cn=LDAP Query\\, Domino Server, OU=Service Accounts,DC=corp,DC=westworlds,DC=com"
AUTH_LDAP_BIND_PASSWORD = "Qu3ryLd@p"
AUTH_LDAP_USER_SEARCH = LDAPSearch('DC=corp,DC=westworlds,DC=com',
                                   ldap.SCOPE_SUBTREE, "(samaccountname=%(user)s)")

AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600
AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_REFERRALS: 0
}

AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'givenname',
    'last_name': 'sn',
    'email': 'mail'
}


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i-63gs#hou6ja0rxqpn7+jyrzp_m2(o0#cyh!#=z76^(c6oxkq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # WebSocket needed packages
    'channels',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'mdta.apps.core',
    'mdta.apps.graphs',
    'mdta.apps.help',
    'mdta.apps.projects',
    'mdta.apps.testcases',
    'mdta.apps.users',
    'mdta.apps.runner',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mdta.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../../templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',

                'mdta.apps.core.views.get_active_top_link',
            ],
        },
    },
]

WSGI_APPLICATION = 'mdta.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SESSION_COOKIE_NAME = 'modelDrivenSessionId'
# Age of session cookies, in seconds
SESSION_COOKIE_AGE = 43200  # 12 hours
# Save the session data on every request
SESSION_SAVE_EVERY_REQUEST = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = 'http://apps.qaci01.wic.west.com/static/'

# Messages error tag
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}
