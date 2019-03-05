#!/bin/sh

gunicorn --bind 0.0.0.0:80 golinks:__hug_wsgi__

#gunicorn --daemon --bind 192.168.11.11:80 --chdir /mnt/sda1/scripts/golinks golinks:__hug_wsgi__
