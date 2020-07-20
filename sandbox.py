import requests

url = 'http://doc.maduma.org/balancer-manager'
r = requests.get(url)
#print(r.status_code, r.encoding)
html_doc = r.text

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')

for link in soup.find_all('h3'):
    print(link)
    for sb in link.next_siblings:
        if sb.name == 'hr':
            break
        if sb.name == 'table':
            print(sb)
