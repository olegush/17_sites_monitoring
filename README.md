# Sites Monitoring Utility

The script checks if website has response code 200 and its expiration date less than 30 days from now.


# Quickstart

Run **check_sites_health.py** with path to text file containing domain names

```bash

$ python check_sites_health.py <filepath>

Server responds (is respond with status 200)
and domains expiration (is domain expires less than 30 days:

DOMAIN                STATUS    EXPIRE
google.com             True     False
google.ua              True     False
google.ru              True     False
google.co              True     False
google.net             True     False
google.us              True     False
google.su              True     False

```


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
