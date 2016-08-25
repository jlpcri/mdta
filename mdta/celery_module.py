import os
import socket
from celery import Celery
from django.conf import settings

if socket.gethostname() in ('sliu-OptiPlex-GX520', 'OM1960L1'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mdta.settings.dev_sliu')
elif socket.gethostname() == 'qaci01':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mdta.settings.qaci01')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mdta.settings.base')

app = Celery('mdta')
app.config_from_object('mdta.celery_config')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, related_name='tasks')