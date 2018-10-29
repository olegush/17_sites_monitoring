import sys
from datetime import datetime
import requests
import socket


def load_urls4check(path):
    with open(path, 'r') as file:
        return file.readlines()


def is_server_respond_with_200(url):
    response = requests.get(url)
    return response.ok


def get_whois_info(whois_server, domain):
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_port = 43
    socket_obj.connect((whois_server, socket_port))
    socket_obj.send(("%s\r\n" % domain).encode("utf-8"))
    socket_data = b''
    bufsize = 4096
    while True:
        try:
            buffer = socket_obj.recv(bufsize)
        except socket.error:
            break
        if buffer:
            socket_data += buffer
        else:
            break
    socket_obj.close()
    return socket_data.decode("utf-8")


def get_domain_expire_date(whois_iana, whois_label, expire_labels, domain):
    whois_info_registrar = get_whois_info(whois_iana, domain)
    for line in whois_info_registrar.split('\n'):
        if line.strip().find(whois_label) == 0:
            registrar = line.rsplit(':')[1].strip()
    for line in get_whois_info(registrar, domain).split('\n'):
        for label in expire_labels:
            if label in line.lower():
                date_expire_string = line.partition(':')[2].strip()[:10]
                return datetime.strptime(date_expire_string, '%Y-%m-%d')


if __name__ == '__main__':
    try:
        filepath = sys.argv[1]
        domains = load_urls4check(filepath)
    except IndexError:
        print('No script parameter (path to txt file)')
    except IOError:
        print('No such file or directory')
    else:
        whois_iana = 'whois.iana.org'
        whois_label = 'whois:'
        expire_labels = ['expiry', 'free', 'expires']
        days_to_expire = 30
        print()
        print('Server responds (is respond with status 200) ')
        print('and domains expiration (is domain expires less than 30 days:')
        print()
        print('{:<20}{:^10}{:^10}'.format('DOMAIN', 'STATUS', 'EXPIRE'))
        for domain in domains:
            domain = domain.strip()
            site = 'http://' + domain.strip()
            is_status_code_200 = str(is_server_respond_with_200(site))
            date_expire = get_domain_expire_date(whois_iana,
                                                 whois_label,
                                                 expire_labels,
                                                 domain)
            is_expire = str((date_expire - datetime.now()).days < 30)
            print('{:<20}{:^10}{:^10}'.format(domain,
                                              is_status_code_200,
                                              is_expire))
