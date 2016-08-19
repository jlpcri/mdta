#!/bin/bash

source /usr/local/bin/virtualenvwrapper.sh

workon mdta

./manage.py loaddata dumpdata/auth.json --settings=mdta.settings.dev_sliu
./manage.py loaddata dumpdata/users.json --settings=mdta.settings.dev_sliu
./manage.py loaddata dumpdata/projects.json --settings=mdta.settings.dev_sliu
./manage.py loaddata dumpdata/graphs.json --settings=mdta.settings.dev_sliu
./manage.py loaddata dumpdata/testcases.json --settings=mdta.settings.dev_sliu
deactivate