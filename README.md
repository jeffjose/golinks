### golinks for your home

## Install

```python
opkg python3 python3-package git

pip3 install -r requirements.txt
```

## Developer mode

```
hug -f golinks.py
```

## Production mode

```
gunicorn --daemon --bind 192.168.11.11:80 --chdir /mnt/sda1/scripts/golinks golinks:__hug_wsgi__
```


## Setup bridge
```
# /jffs/scripts/services-start

ifconfig br0:1 192.168.11.11 netmask 255.255.255.0 up
or
ip address add 192.168.11.11/24 dev br0

```

# Add entry to /etc/hosts
```

192.168.11.11 go

ifconfig up && ifconfig down
```

## Flush DNS cache on ubuntu
```
sudo systemctl restart systemd-resolved.service ; sudo systemd-resolve --flush-caches ; sudo systemd-resolve --statistics
```
