from bs4 import BeautifulSoup
import requests


def autoru_parse(n):
    name = 'https://auto.ru/sankt-peterburg/cars/{}/all/'.format(n)
    r = requests.get(name)
    r.encoding = 'utf8'
    soup = BeautifulSoup(r.text, 'html.parser')
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
        else:
            price = 0
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
    return list_of_cars


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
    proxy = {'http': 'http://' + '176.9.119.170:8080'}
    with open('us_ag.txt', 'r') as f:
        for i in map(str.strip, f.readlines()):
            usr_ag = {'User-Agent': i}
            r = requests.get(name, proxies=proxy, headers=usr_ag)
            if str(r.status_code)[0] == '2':
                break
    r.encoding = 'utf8'
    soup = BeautifulSoup(r.text, 'html.parser')
    list_of_cars = []
    print(r.status_code, i)
    print(soup)
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
    return list_of_cars


'''with open('car.json', mode='w') as wr:''' #json
'''s = str(list_of_cars).replace("'", '"')
s = s.replace('}, {', '},\n{')
wr.write(s)''' #json