import logging
import requests
from bs4 import BeautifulSoup

def get_status(addr, group, proto='https'):
    html = get_html(addr, proto)
    status = parse_html(html)
    return status[group]

def get_html(addr, proto):
    lb_manager_url = f'{proto}://{addr}/balancer-manager'
    response = requests.get(lb_manager_url)
    if response.status_code == 200:
        html = response.text
    else:
        logging.error(response.reason)
        html = None
    return html

def parse_html(html):
    status = {}
    soup = BeautifulSoup(html, 'html.parser')
    for group_h3 in soup.find_all('h3'):
        _, group_name = group_h3.find('a').string.split('://')
        _, members_table = group_h3.find_next_siblings('table', limit=2)
        _, *members_raws = members_table.find_all('tr')
        status[group_name] = []
        for raw in members_raws:
            *_, status_td = raw.find_all('td', limit=6)
            member_status = status_td.string.strip()
            status[group_name].append(member_status)
    return status

def set_worker(addr, group, worker, disable, proto='https'):
    pass

