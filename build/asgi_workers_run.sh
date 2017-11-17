#!/usr/bin/env bash

source /usr/local/bin/virtualenvwrapper.sh
workon mdta

python manage.py runworker --settings=mdta.settings.dev_sliu
