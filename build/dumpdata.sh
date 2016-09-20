#!/bin/bash

source /usr/local/bin/virtualenvwrapper.sh

workon mdta

./manage.py dumpdata auth.User auth.Group > dumpdata/auth.json --indent 4 --settings=mdta.settings.dev_sliu
./manage.py dumpdata users > dumpdata/users.json --indent 4 --settings=mdta.settings.dev_sliu
./manage.py dumpdata projects > dumpdata/projects.json --indent 4 --settings=mdta.settings.dev_sliu
./manage.py dumpdata graphs > dumpdata/graphs.json --indent 4 --settings=mdta.settings.dev_sliu
./manage.py dumpdata testcases > dumpdata/testcases.json --indent 4 --settings=mdta.settings.dev_sliu
deactivate