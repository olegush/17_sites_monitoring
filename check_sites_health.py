import sys
from datetime import datetime
import requests
import whois


def load_strings_urls(path):
    with open(path, 'r') as file:
        return file.readlines()


def is_server_respond_ok(url):
    response = requests.get(url)
    return response.ok


def get_domain_expire_date(domain):
    whois_data = whois.whois(domain)
    if isinstance(whois_data['expiration_date'], list):
        return whois_data['expiration_date'][0]
    else:
        return whois_data['expiration_date']


if __name__ == '__main__':
    try:
        filepath = sys.argv[1]
        sites = load_strings_urls(filepath)
    except IndexError:
        print('No script parameter (path to txt file)')
    except IOError:
        print('No such file or directory')
    else:
        days_to_expire = 30
        print('\nServer responds (is respond with status 200) ')
        print('and domains expiration (is domain expires less than 30 days:\n')
        print('{:<25}{:^10}{:^10}'.format('SITE', 'STATUS', 'EXPIRE'))
        for site in sites:
            site = site.strip()
            domain = site.partition('//')[2].replace('www.', '')
            date_expire = get_domain_expire_date(domain)
            is_expire = (date_expire - datetime.now()).days < 30
            print('{:<25}{:^10}{:^10}'.format(site,
                                              is_server_respond_ok(site),
                                              is_expire
                                              ))
