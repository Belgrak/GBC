from bs4 import BeautifulSoup
import requests

r = requests.get('https://www.avito.ru/sankt-peterburg/avtomobili?cd=1&radius=0')

soup = BeautifulSoup(r.text, 'html.parser')
print('\n'.join(['<option>{}</option>'.format(i.text) for i in soup.select('.popular-rubricator-row-2oc-J a')]))