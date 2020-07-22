import logging
import requests
from bs4 import BeautifulSoup

def get_status(addr, group, proto='https'):
    html = get_html(addr, proto)
    status = parse_html(html)
    return [x['status'] for x in status[group]['workers']]

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
        html_a = group_h3.a
        _, group_name = html_a.string.split('://')
        _, nonce = html_a['href'].split('nonce=')
        _, members_table = group_h3.find_next_siblings('table', limit=2)
        _, *members_raws = members_table.find_all('tr')
        status[group_name] = {'nonce': nonce, 'workers': []}
        for raw in members_raws:
            worker_td, *_, status_td = raw.find_all('td', limit=6)
            worker_url = worker_td.a.string.strip()
            member_status = status_td.string.strip()
            status[group_name]['workers'].append({
                'url': worker_url,
                'status': member_status,
                })
    return status

def set_worker(addr, group, worker, disable, proto='https'):
    pass

