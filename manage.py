#!/usr/bin/env python
import os
import socket
import sys

from mdta.asgi import get_django_settings_module

if __name__ == "__main__":
    settings_name = get_django_settings_module(socket.gethostname())
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_name)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
