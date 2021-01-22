from bs4 import BeautifulSoup
import requests


class Car_Parse():
    def __init__(self, n):
        self.name_of_car = n

    def autoru_parse(self):
        name = 'https://auto.ru/sankt-peterburg/cars/{}/all/'.format(self.name_of_car)
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


'''with open('car.json', mode='w') as wr:''' #json
'''s = str(list_of_cars).replace("'", '"')
s = s.replace('}, {', '},\n{')
wr.write(s)''' #json