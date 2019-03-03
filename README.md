### golinks for your home


## Install

```python
pip3 install hug, simplejson, path.py, gunicorn
```


## Developer mode
```
hug -f golinks.py
```

## Production mode
```
gunicorn --bind 0.0.0.0:8000 golinks:__hug_wsgi__
```
