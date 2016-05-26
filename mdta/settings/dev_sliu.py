__author__ = 'sliu'
from mdta.settings.base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mdta',
        'USER': 'scorecard',
        'PASSWORD': 'scorecard_development',
        'HOST': 'qaci01.wic.west.com',
        'PORT': '5432',
    }
}
