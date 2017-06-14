#!/usr/bin/env python
import os
import socket
import sys

if __name__ == "__main__":
    if socket.gethostname() == 'alpha':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mdta.settings.dev_mohan")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mdta.settings.dev_mohan")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
