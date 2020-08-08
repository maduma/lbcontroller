import logging
import requests
from bs4 import BeautifulSoup

def get_group_status(addr, group, proto='https'):
    html = get_html(addr, proto)
    if not html:
        return 'error', f'cannot connect to loadbalancer {addr}'

    status = parse_html(html)
    if not group in status:
        return 'error', f'no group {group} in loadbalancer {addr}'

    workers_status = [ x['status'] for x in status[group]['workers'] ]
    unique_status = set([ x == 'Init Ok' for x in workers_status ])
    if len(unique_status) == 1:
        if unique_status.pop():
            return 'ok', workers_status 
        else:
            return 'nok', workers_status
    return 'degraded', workers_status

def get_html(addr, proto):
    lb_manager_url = f'{proto}://{addr}/balancer-manager'
    html = None
    try:
        response = requests.get(lb_manager_url, timeout=5)
        if response.status_code == 200:
            html = response.text
        else:
            logging.error(response.reason)
    except Exception as e:
        logging.error(e)
        logging.error(f'Cannot connect to loadbalancer {lb_manager_url}')
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
    if not html:
        return False

    status = parse_html(html)
    if group in status and len(status[group]['workers']) > workerid:
        try:
            response = requests.post(lb_manager_url, data={
                'w': status[group]['workers'][workerid]['url'],
                'b': group,
                'nonce': status[group]['nonce'],
                'w_status_D': 1 if disable else 0,
            })
            if response.status_code == 200:
                return True
            else:
                logging.error(f'Cannot POST to loadbalancer {lb_manager_url}')
                logging.error(response.reason)
        except Exception as e:
            logging.error(f'Cannot connect to loadbalancer {lb_manager_url}')
            logging.error(e)

    else:
        logging.error(f'Cannot get group and/or instance in loadbalancer')
        logging.error(status)

    return False
