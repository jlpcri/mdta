__author__ = 'sliu'
from mdta.settings.base import *

SETTINGS_MODULE = 'mdta.settings.qaci01'

ALLOWED_HOSTS = [
    'apps.qaci01.wic.west.com',
    'apps.qaci01'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mdta',
        'USER': 'scorecard',
        'PASSWORD': 'scorecard_development',
        'HOST': 'qaci01.wic.west.com',
        'PORT': '5433'  # Version 9.4.4
    }
}
