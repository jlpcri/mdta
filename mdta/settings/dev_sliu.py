__author__ = 'sliu'
from mdta.settings.base import *

DEBUG = True
INSTALLED_APPS += ['debug_toolbar', ]
MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
INTERNAL_IPS = ['127.0.0.1', '10.6.20.127', '10.27.170.225']

DB_DEFAULT = {
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

DB_AWS_PG = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mdta',
        'USER': 'ceeq',
        'PASSWORD': 'ceeq_development',
        'HOST': 'pginstance.ce8tamiymyr9.us-west-2.rds.amazonaws.com',
        'PORT': '5432'
    }
}

DB_AWS_SQLITE3 = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mysqldb',
        'USER': 'ceeq',
        'PASSWORD': 'ceeq_development',
        'HOST': 'mysqlinstance.ce8tamiymyr9.us-west-2.rds.amazonaws.com',
        'PORT': '3306'
    }
}

DATABASES = DB_DEFAULT
