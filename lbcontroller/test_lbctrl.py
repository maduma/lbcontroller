from lbcontroller import lbctrl
import httpretty


def test_get_group_status():
    addr = 'doc.maduma.org'

    filename = 'status_html/lb_status_pia_ok_ok_pom_err_ok.html'
    with open(filename, 'r') as f: html = f.read()
    lb_manager_url = f'http://{addr}/balancer-manager'

    httpretty.enable()
    httpretty.register_uri(httpretty.GET, lb_manager_url, body=html)

    status = lbctrl.get_group_status(addr, 'pianiste', proto='http')
    assert status == ('ok', ['Init Ok', 'Init Ok'])
    status = lbctrl.get_group_status(addr, 'pompiste', proto='http')
    assert status == ('degraded', ['Init Err', 'Init Ok'])

    httpretty.disable()
    httpretty.reset()

def test_get_group_status_with_auth():
    addr = 'doc.maduma.org'
    lb_manager_url = f'http://{addr}/balancer-manager'
    auth_header = 'Basic YWRtaW46YWRtaW4='

    httpretty.enable()
    httpretty.register_uri(httpretty.GET, lb_manager_url)

    status = lbctrl.get_group_status(addr, 'pianiste', proto='http', auth=('admin', 'admin'))
    assert httpretty.last_request().headers['Authorization'] == auth_header
    
    httpretty.disable()
    httpretty.reset()

def test_parse_html():
    filename = 'status_html/lb_status_ok.html'
    with open(filename, 'r') as f: html = f.read()
    assert lbctrl.parse_html(html) == {
            'pianiste': { 
                'nonce': 'c4718cc9-b73a-4659-86a5-ceeb758f0160',
                'workers': [
                    {'url': 'http://acc1.maduma.org/pianiste-metrics:80', 'status': 'Init Ok'},
                    {'url': 'http://acc2.maduma.org/pianiste-metrics:80', 'status': 'Init Ok'},
                    ],
                },
            'pompiste': { 
                'nonce': 'bc9300f7-7902-467f-953c-6e6c57f8303f',
                'workers': [
                    {'url': 'http://acc1.maduma.org/pompiste-metrics:80', 'status': 'Init Ok'},
                    {'url': 'http://acc2.maduma.org/pompiste-metrics:80', 'status': 'Init Ok'},
                    ],
                },
            }

    filename = 'status_html/lb_status_pia_err_err_pom_ok_err.html'
    with open(filename, 'r') as f: html = f.read()
    assert lbctrl.parse_html(html) == {
            'pianiste': { 
                'nonce': 'c4718cc9-b73a-4659-86a5-ceeb758f0160',
                'workers': [
                    {'url': 'http://acc1.maduma.org/pianiste-metrics:80', 'status': 'Init Err'},
                    {'url': 'http://acc2.maduma.org/pianiste-metrics:80', 'status': 'Init Err'},
                    ],
                },
            'pompiste': { 
                'nonce': 'bc9300f7-7902-467f-953c-6e6c57f8303f',
                'workers': [
                    {'url': 'http://acc1.maduma.org/pompiste-metrics:80', 'status': 'Init Ok'},
                    {'url': 'http://acc2.maduma.org/pompiste-metrics:80', 'status': 'Init Err'},
                    ],
                },
            }

def test_disable_worker():
    addr = 'doc.maduma.org'
    group = 'pompiste'
    workerid = 1

    filename = 'status_html/lb_status_ok.html'
    with open(filename, 'r') as f: html = f.read()
    lb_manager_url = f'http://{addr}/balancer-manager'

    httpretty.enable()
    httpretty.register_uri(httpretty.GET, lb_manager_url, body=html)
    httpretty.register_uri(httpretty.POST, lb_manager_url)

    lbctrl.set_worker(addr, group, workerid, disable=True, proto='http')
    req = httpretty.last_request()
    assert req.method == 'POST'
    assert req.parsed_body == {
        'w': ['http://acc2.maduma.org/pompiste-metrics:80'],
        'b': ['pompiste'],
        'nonce': ['bc9300f7-7902-467f-953c-6e6c57f8303f'],
        'w_status_D': ['1'],
    }

    httpretty.disable()
    httpretty.reset()

def test_enable_worker():
    addr = 'doc.maduma.org'
    group = 'pianiste'
    workerid = 0

    filename = 'status_html/lb_status_ok.html'
    with open(filename, 'r') as f: html = f.read()
    lb_manager_url = f'http://{addr}/balancer-manager'

    httpretty.enable()
    httpretty.register_uri(httpretty.GET, lb_manager_url, body=html)
    httpretty.register_uri(httpretty.POST, lb_manager_url)

    lbctrl.set_worker(addr, group, workerid, disable=False, proto='http')
    req = httpretty.last_request()
    assert req.method == 'POST'
    assert req.parsed_body == {
        'w': ['http://acc1.maduma.org/pianiste-metrics:80'],
        'b': ['pianiste'],
        'nonce': ['c4718cc9-b73a-4659-86a5-ceeb758f0160'],
        'w_status_D': ['0'],
    }

    httpretty.disable()
    httpretty.reset()

def test_enable_worker_with_auth():
    addr = 'doc.maduma.org'
    group = 'pianiste'
    workerid = 0
    auth_header = 'Basic YWRtaW46YWRtaW4='

    filename = 'status_html/lb_status_ok.html'
    with open(filename, 'r') as f: html = f.read()
    lb_manager_url = f'http://{addr}/balancer-manager'

    httpretty.enable()
    httpretty.register_uri(httpretty.GET, lb_manager_url, body=html)
    httpretty.register_uri(httpretty.POST, lb_manager_url)

    lbctrl.set_worker(addr, group, workerid, disable=False, proto='http', auth=('admin', 'admin'))

    assert httpretty.last_request().method == 'POST'
    assert httpretty.last_request().headers['Authorization'] == auth_header
    httpretty.disable()
    httpretty.reset()
