#!/bin/sh

gunicorn --bind 0.0.0.0:80 golinks:__hug_wsgi__

#gunicorn --bind 0.0.0.0:80 --chdir /path/to/the/source/code golinks:__hug_wsgi__
