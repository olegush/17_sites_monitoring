# Sites Monitoring Utility

The script checks if website has response code 200 and its expiration date less than 30 days from now.

# How to Install

Python 3, **requests** and **whois** modules should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

# Quickstart

Run **check_sites_health.py** with path to text file containing domain names

```bash

$ python check_sites_health.py <filepath>

Server responds (is respond with status 200)
and domains expiration (is domain expires less than 30 days:

SITE                       STATUS    EXPIRE
http://www.google.com        1         0
http://google.ru             1         0
http://google.co             1         0
http://google.net            1         0
http://www.google.us         1         0
http://www.google.su         1         0

```


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
