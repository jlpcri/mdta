from mdta.settings.base import *

DEBUG = True
INSTALLED_APPS += ['debug_toolbar', ]
MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
INTERNAL_IPS = ['10.6.20.124','127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mdta',
        'USER': 'scorecard',
        'PASSWORD': 'scorecard_development',
        'HOST': 'qaci01.wic.west.com',
        'PORT': '5433',
    }
}

'''DB_6437 = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mdta',
        'USER': 'ceeq',
        'PASSWORD': 'FkhfDhPx%A=-?h_snCMuQ$&%5crcx%tpxw24pVVp+U-UrXs4q6=uK=8^-evN-RxA',
        'HOST': 'linux6437.wic.west.com',
        'PORT': '5433'   # posgtres 9.4 instance
    }
}

DATABASES = DB_6437
'''
