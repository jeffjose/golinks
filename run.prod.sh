#!/bin/sh

gunicorn --bind 0.0.0.0:80 golinks:__hug_wsgi__
