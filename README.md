### golinks for your home

## Install

```python
opkg python3 python3-package git

pip3 install setuptools
pip3 install hug
pip3 install simplejson
pip3 install path.py
pip3 install gunicorn
```

## Developer mode

```
hug -f golinks.py
```

## Production mode

```
gunicorn --bind 0.0.0.0:8000 golinks:__hug_wsgi__
```
