#!/bin/sh

virtualenv --no-site-packages --clear env
. /usr/local/virtualenvs/mdta/bin/activate

pip install --download /tmp/jenkins/pip-cache -r requirements/jenkins.txt

python manage.py jenkins --enable-coverage --settings=mdta.settings.jenkins