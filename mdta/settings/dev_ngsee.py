import socket
from mdta.settings.base import *

DEBUG = True
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
INSTALLED_APPS += ['debug_toolbar', ]
MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
INTERNAL_IPS = ['127.0.0.1', '10.6.20.97', '10.6.20.60']

if socket.gethostname() == 'OM1006L1':
    CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [('10.6.20.97', 6379)]

QACI = {
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

DATABASES = DB_6437