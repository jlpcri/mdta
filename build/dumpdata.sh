#!/bin/bash

source /usr/local/bin/virtualenvwrapper.sh

workon mdta

./manage.py dumpdata auth.User auth.Group > dumpdata/auth.json --settings=mdta.settings.dev_sliu
./manage.py dumpdata users > dumpdata/users.json --settings=mdta.settings.dev_sliu
./manage.py dumpdata projects > dumpdata/projects.json --settings=mdta.settings.dev_sliu
./manage.py dumpdata graphs > dumpdata/graphs.json --settings=mdta.settings.dev_sliu
./manage.py dumpdata testcases > dumpdata/testcases.json --settings=mdta.settings.dev_sliu
deactivate