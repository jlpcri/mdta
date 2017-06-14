from mdta.settings.base import *

DEBUG = True
INSTALLED_APPS += ['debug_toolbar', ]
MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
INTERNAL_IPS = ['127.0.0.1', '10.6.20.124']

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
