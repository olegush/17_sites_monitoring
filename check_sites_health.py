import os.path
import argparse
from datetime import datetime
import requests
import whois


def get_args_parser():
    parser = argparse.ArgumentParser(description='Sites Monitoring Utility')
    parser.add_argument('filepath', help='path to file with urls')
    parser.add_argument('--days',
                        help='days to expire, 30 by default',
                        type=int,
                        default=30
                        )
    args = parser.parse_args()
    return args


def load_strings_urls(path):
    with open(path, 'r') as file:
        return file.read().splitlines()


def is_server_respond_ok(url):
    try:
        response = requests.get(url)
        return response.ok
    except requests.ConnectionError:
        return False


def get_domain_expiration_date(url):
    whois_data = whois.whois(url)
    if isinstance(whois_data['expiration_date'], list):
        date_expire = whois_data['expiration_date'][0]
    else:
        date_expire = whois_data['expiration_date']
    return date_expire


if __name__ == '__main__':
    user_args = get_args_parser()
    days_to_expire = user_args.days
    filepath = user_args.filepath
    if not filepath:
        exit('No script parameter (path to txt file)')
    if not os.path.isfile(filepath):
        exit('No such file')
    urls = load_strings_urls(filepath)
    print('\nServer responds (is respond with status OK) and \ndomains '
          'expiration (is domain expires less than {} days:\n'
          .format(days_to_expire))
    print('{:<25}{:^10}{:^10}'.format('SITE', 'STATUS', 'EXPIRE'))
    for url in urls:
        status_ok = is_server_respond_ok(url)
        date_expire = get_domain_expiration_date(url)
        date_now = datetime.now()
        if status_ok and date_expire:
            status_expire = (date_expire - date_now).days < days_to_expire
        else:
            status_expire = 'no data'
        print('{:<25}{:^10}{:^10}'.format(url, status_ok, status_expire))
