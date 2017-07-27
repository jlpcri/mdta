#!/bin/bash

# This script for running celery on local desktop
# required: 'sudo apt-get install rabbitmq-server'

source /usr/local/bin/virtualenvwrapper.sh
workon mdta

celery worker -n %h.mdta -A mdta -Q mdta_queue -l info