import os
import socket
from channels.asgi import get_channel_layer


def get_django_settings_module(hostname):
    data = 'mdta.settings.'

    if hostname in ('sliu-OptiPlex-GX520', 'OM1960L1'):
        data += 'dev_sliu'
    elif hostname == 'alpha':
        data += "dev_heyden"
    elif hostname == "sigma":
        data += "sigma"
    elif hostname == 'qaci01':
        data += 'qaci01'
    else:
        data += 'base'

    return data


settings_name = get_django_settings_module(socket.gethostname())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_name)

channel_layer = get_channel_layer()
