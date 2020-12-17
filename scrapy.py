from bs4 import BeautifulSoup
import requests
import lxml

r = requests.get('https://yandex.ru/pogoda/?lat=59.849594&lon=30.276674&utm_campaign=informer&utm_content=main_informer&utm_medium=web&utm_source=home&utm_term=title')
bs = BeautifulSoup(r.content, 'lxml')

print(bs.select_one('a').select_one('::attr(href)'))