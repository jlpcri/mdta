#!/bin/bash

source /usr/local/bin/virtualenvwrapper.sh

workon mdta

./manage.py loaddata dumpdata/auth.json
./manage.py loaddata dumpdata/users.json
./manage.py loaddata dumpdata/projects.json
./manage.py loaddata dumpdata/graphs.json
./manage.py loaddata dumpdata/testcases.json
deactivate