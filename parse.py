from bs4 import BeautifulSoup
import requests
'''
r_wik = requests.get('https://ru.wikipedia.org/wiki/Коды_субъектов_Российской_Федерации')
soup_wik = BeautifulSoup(r_wik.text, 'html.parser')
for j in soup_wik.find_all('tr')[1:]:
    if j.select_one('td'):
        if 'Крым' in j.select('td')[0].text:
            print('"{}": {}'.format(j.select('td')[0].text, '82'), end=', ')
        else:
            print('"{}": {}'.format(j.select('td')[0].text, str(int(j.select('td')[2].text.split(', ')[0]))), end=', ')
exit()
'''



def autoru_parse(n, page, sor, city):
    if n == 'rolls-royce':
        n = 'rolls_royce'
    if sor == 'По умолчанию':
        sor = ''
    if sor == 'По цене ↑':
        sor = '&sort=price-asc'
    if sor == 'По цене ↓':
        sor = '&sort=price-desc'
    name = 'https://auto.ru/{}/cars/{}/all/?page={}{}'.format(city, n, page, sor)
    r = requests.get(name)
    if r.status_code == 200:
        r.encoding = 'utf8'
        soup = BeautifulSoup(r.text, 'html.parser')
        if len(soup.select('[role="link"]')) >= 3:
            count_of_pages = soup.select('[role="link"]')[-3].text
        else:
            count_of_pages = '1'
        list_of_cars = []
        for i in soup.select('.ListingItem-module__main'):
            motor = i.select_one('.ListingItemTechSummaryDesktop__cell')
            km_age = i.select_one('.ListingItem-module__kmAge')
            year = i.select_one('.ListingItem-module__year')
            link = i.select_one('.ListingItemTitle-module__link')
            photo = i.select_one('.Brazzers__image')
            price = i.select_one('.ListingItemPrice-module__content')
            if price:
                price = price.text
                if 'от' in price:
                    price = ''.join(price.split()[1:])
            else:
                price = '0₽'
            if photo != None:
                list_of_cars.append({
                    'title': link.text,
                    'link': link['href'],
                    'photo': 'http:' + photo['data-src'],
                    'year': year.text,
                    'km': km_age.text,
                    'motor': motor.text,
                    'price': price
                })
            else:
                list_of_cars.append({
                    'title': link.text,
                    'link': link['href'],
                    'photo': 0,
                    'year': year.text,
                    'km': km_age.text,
                    'motor': motor.text,
                    'price': price
                })
        return list_of_cars, count_of_pages
    else:
        return []

'''
def proxy_us_ag():
    r = requests.get('https://hidemy.name/ru/proxy-list/')
    soup = BeautifulSoup(r.text, 'html.parser')
    sp = []
    print(soup.select('.table_block'))
    for i in soup.select('.table_block tbody tr'):
        print(i)
        sp.append(':'.join([t.text for t in i.select('td')]))
    print(sp)


def avito_parse(n):
    if n == 'mercedes':
        n = 'mercedes-benz'
    if n == 'vaz':
        n = 'vaz_lada'
    name = 'https://www.avito.ru/sankt-peterburg/avtomobili/{}'.format(n)
    with open('us_ag.txt', 'r') as f:
        with open('proxy.txt', 'r') as pr:
            for i in map(str.strip, f.readlines()):
                for t in map(str.strip, pr.readlines()):
                    usr_ag = {'User-Agent': i}
                    proxy = {'http': 'http://' + t}
                    r = requests.get(name, proxies=proxy, headers=usr_ag)
                    print(str(r.status_code)[0])
                    if str(r.status_code)[0] == '2':
                        r.encoding = 'utf8'
                        soup = BeautifulSoup(r.text, 'html.parser')
                        print(soup.select_one('title').text)
            exit()
    r.encoding = 'utf8'
    soup = BeautifulSoup(r.text, 'html.parser')
    list_of_cars = []
    print(r.status_code)
    print(proxy, usr_ag)
    for i in soup.select('[data-marker="item"]'):
        km_motor = i.select('[data-marker="item-specific-params"]')[0]
        link = i.select('a')[1]
        photo = i.select_one('img')
        print(photo)
        price = i.select_one('[class|="price-text"]')
        if len(km_motor.text.split(', ')) < 5:
            km = 'Новая'
            motor = km_motor.text.split(', ')[0]
        else:
            km = km_motor.text.split(', ')[0]
            motor = km_motor.text.split(', ')[1]
        if not price:
            price = 0
        if photo != None:
            list_of_cars.append({
                'title': link.text.split(', ')[0],
                'link': 'https://www.avito.ru' + link['href'],
                'photo': photo['src'],
                'year': link.text.split(', ')[1],
                'km': km,
                'motor': motor,
                'price': price.text
            })
        else:
            list_of_cars.append({
                'title': link.text.split(', ')[0],
                'link': 'https://www.avito.ru' + link['href'],
                'photo': 0,
                'year': link.text.split(', ')[1],
                'km': km,
                'motor': motor,
                'price': price.text
            })
    return list_of_cars'''


def drom_parse(n, page, sor, city):
    if n == 'mercedes':
        n = 'mercedes-benz'
    if n == 'vaz':
        n = 'lada'
    if sor == 'По умолчанию':
        sor = ''
    if sor == 'По цене ↑':
        sor = '?order=price'
    if sor == 'По цене ↓':
        sor = '?order=price&order_d=desc'
    name = 'https://auto.drom.ru/region{}/{}/all/page{}/{}'.format(city, n, page, sor)
    r = requests.get(name)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        if soup.select('[data-ftid="component_pagination-item"]'):
            count_of_pages = soup.select('[data-ftid="component_pagination-item"]')[-1].text
        else:
            count_of_pages = '1'
        list_of_cars = []
        for i in soup.select('[data-ftid="bulls-list_bull"]'):
            desc = i.select_one('[data-ftid="bull_description"]').text.split(', ')
            title = i.select_one('[data-ftid="bull_title"]').text.split(', ')
            photo = i.select_one('[data-ftid="bull_image"] img')
            price = i.select_one('[data-ftid="bull_price"]')
            if price:
                price = price.text
                if 'от' in price:
                    price = ''.join(price.split()[1:])
            else:
                price = '0₽'
            if 'км' in desc[-1]:
                km_age = desc[-1]
            else:
                km_age = ''
            if photo != None:
                list_of_cars.append({
                    'title': title[0],
                    'link': i['href'],
                    'photo': photo['data-srcset'].split()[0],
                    'year': title[1],
                    'km': km_age,
                    'motor': desc[0],
                    'price': price + '₽'
                })
            else:
                list_of_cars.append({
                    'title': title[0],
                    'link': i['href'],
                    'photo': 0,
                    'year': title[1],
                    'km': km_age,
                    'motor': desc[0],
                    'price': price + '₽'
                })
        return list_of_cars, count_of_pages
    else:
        return []



'''with open('car.json', mode='w') as wr:''' #json
'''s = str(list_of_cars).replace("'", '"')
s = s.replace('}, {', '},\n{')
wr.write(s)''' #json