from bs4 import BeautifulSoup
import requests


class Car_Parse():
    def __init__(self, n):
        self.r = requests.get(n)
        self.r.encoding = 'utf8'
        self.soup = BeautifulSoup(self.r.text, 'html.parser')
        self.sp = []
        print(self.soup.select('.ListingPagination-module__container a')[-3])

    def parse(self):
        for i in self.soup.select('.ListingItem-module__main'):
            link = i.select_one('.ListingItemTitle-module__link')
            photo = i.select_one('.Brazzers__image')
            price = i.select_one('.ListingItemPrice-module__content')
            if price:
                price = price.text
            else:
                price = 0
            print(photo)
            if photo != None:
                self.sp.append({
                    'title': link.text,
                    'link': link['href'],
                    'photo': 'http:' + photo['data-src'],
                    'price': price
                })
            else:
                self.sp.append({
                    'title': link.text,
                    'link': link['href'],
                    'photo': 0,
                    'price': price
                })
        return self.sp

print(Car_Parse('https://auto.ru/sankt-peterburg/cars/uaz/all/').parse())
'''with open('car.json', mode='w') as wr:''' #json
'''s = str(sp).replace("'", '"')
s = s.replace('}, {', '},\n{')
wr.write(s)''' #json