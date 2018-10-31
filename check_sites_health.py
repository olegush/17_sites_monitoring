import os.path
import argparse
from datetime import datetime
import requests
import whois


def parser_args():
    parser = argparse.ArgumentParser(description='Sites Monitoring Utility')
    parser.add_argument('filepath', help='path to file with urls')
    parser.add_argument('--days',
                        help='days to expire, 30 by default',
                        type=int)
    args = parser.parse_args()
    return args


def load_strings_urls(path):
    with open(path, 'r') as file:
        return file.read().splitlines()


def is_server_respond_ok(url):
    response = requests.get(url)
    return response.ok


def get_domain_is_expire(domain, days_to_expire):
    whois_data = whois.whois(domain)
    if not whois_data['expiration_date']:
        return '-'
    elif isinstance(whois_data['expiration_date'], list):
        date_expire = whois_data['expiration_date'][0]
    else:
        date_expire = whois_data['expiration_date']
    return (date_expire - datetime.now()).days < days_to_expire


if __name__ == '__main__':
    whois_args = parser_args()
    days_to_expire = whois_args.days
    filepath = whois_args.filepath
    if not filepath:
        exit('No script parameter (path to txt file)')
    if not os.path.isfile(filepath):
        exit('No such file')
    if not days_to_expire:
        days_to_expire = 30
    urls = load_strings_urls(filepath)
    print('\nServer responds (is respond with status OK) and \ndomains '
          'expiration (is domain expires less than {} days:\n'
          .format(days_to_expire))
    print('{:<25}{:^10}{:^10}'.format('SITE', 'STATUS', 'EXPIRE'))
    for url in urls:
        is_ok = is_server_respond_ok(url)
        is_expire = get_domain_is_expire(url, days_to_expire)
        print('{:<25}{:^10}{:^10}'.format(url, is_ok, is_expire))
