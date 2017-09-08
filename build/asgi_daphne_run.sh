#!/usr/bin/env bash

source /usr/local/bin/virtualenvwrapper.sh
workon mdta

daphne mdta.asgi:channel_layer --bind 0.0.0.0 --port 9901
