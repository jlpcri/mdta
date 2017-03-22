#!/bin/bash

docker-compose run web ./manage.py migrate --settings=mdta.settings.dev_uno

docker-compose run web ./manage.py loaddata dumpdata/docker/auth.json --settings=mdta.settings.dev_uno
docker-compose run web ./manage.py loaddata dumpdata/docker/users.json --settings=mdta.settings.dev_uno
docker-compose run web ./manage.py loaddata dumpdata/docker/projects.json --settings=mdta.settings.dev_uno
docker-compose run web ./manage.py loaddata dumpdata/docker/graphs.json --settings=mdta.settings.dev_uno
docker-compose run web ./manage.py loaddata dumpdata/docker/testcases.json --settings=mdta.settings.dev_uno

