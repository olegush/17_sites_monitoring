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


def get_domain_expire_date(domain):
    whois_data = whois.whois(domain)
    if not whois_data['expiration_date']:
        return 'no data'
    elif isinstance(whois_data['expiration_date'], list):
        return whois_data['expiration_date'][0]
    else:
        return whois_data['expiration_date']


if __name__ == '__main__':
    args = parser_args()
    days_to_expire = args.days
    filepath = args.filepath
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
        date_expire = get_domain_expire_date(url)
        if date_expire == 'no data':
            is_expire = '-'
        else:
            is_expire = (date_expire - datetime.now()).days < days_to_expire
        print('{:<25}{:^10}{:^10}'
              .format(url, is_server_respond_ok(url), is_expire))
