__author__ = 'sliu'
from mdta.settings.base import *

DEBUG = True

DB_QACI01 = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mdta',
        'USER': 'scorecard',
        'PASSWORD': 'scorecard_development',
        'HOST': 'qaci01.wic.west.com',
        # 'PORT': '5432', #  Version 9.1.10
        'PORT': '5433'  # Version 9.4.4
    }
}

DB_6437 = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mdta',
        'USER': 'ceeq',
        'PASSWORD': 'FkhfDhPx%A=-?h_snCMuQ$&%5crcx%tpxw24pVVp+U-UrXs4q6=uK=8^-evN-RxA',
        'HOST': 'linux6437.wic.west.com',
        'PORT': '5433'   # posgtres 9.4 instance
    }
}


DATABASES = DB_QACI01
