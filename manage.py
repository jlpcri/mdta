#!/usr/bin/env python
import os
import socket
import sys

if __name__ == "__main__":
    if socket.gethostname() == 'QAIMint':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mdta.settings.dev_heyden")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mdta.settings.base")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
