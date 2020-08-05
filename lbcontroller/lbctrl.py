import logging
import requests
from bs4 import BeautifulSoup

def get_group_status(addr, group, proto='https'):
    html = get_html(addr, proto)
    status = parse_html(html)
    workers_status = [ x['status'] for x in status[group]['workers'] ]
    workers_ok = set([ x == 'Init Ok' for x in workers_status ])
    if len(workers_ok) == 1:
        if workers_ok.pop():
            return 'ok' 
        else:
            return 'nok', workers_status
    return 'degraded', workers_status

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

def set_worker(addr, group, workerid, disable, proto='https'):
    lb_manager_url = f'{proto}://{addr}/balancer-manager'
    html = get_html(addr, proto)
    status = parse_html(html)
    if group in status and  workerid in status[group]['workers']:
        response = requests.post(lb_manager_url, data={
            'w': status[group]['workers'][workerid]['url'],
            'b': group,
            'nonce': status[group]['nonce'],
            'w_status_D': 1 if disable else 0,
        })
        if response.status_code != 200:
            logging.error(response.reason)
    else:
        logging.error(group)
