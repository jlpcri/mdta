from mdta.settings.base import *

DEBUG = True
INSTALLED_APPS += ['debug_toolbar', ]
MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
INTERNAL_IPS = ['127.0.0.1', '10.6.20.90', '10.6.20.91', '10.6.20.121', '10.27.168.217', '10.6.20.112']

DB_DEFAULT = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mdta',
        'USER': 'scorecard',
        'PASSWORD': 'scorecard_development',
        'HOST': 'qaci01.wic.west.com',
        'PORT': '5433',
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

DB_LOCAL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mdta',  # test_mdta',
        'USER': 'postgres',  # ewhitcomb',
        'PASSWORD': 'visilog',
        'HOST': '127.0.0.1',  # '10.6.20.90',
        'PORT': '5432',  # 2049',
    }
}


DATABASES = DB_LOCAL
#./manage.py runserver 0.0.0.0:8000 --settings=mdta.settings.dev_cmorris
# remove/coment out any for X in objects
#
