from flask import Flask, request, render_template, make_response
from parse import *
import random

from setsAndConsts import dic, region_dic

app = Flask(__name__)


@app.route('/cars')
def get():
    page = request.args.get('page', default='1', type=str)
    brand = request.args.get('marka', default='', type=str)
    sort = request.args.get('sort', default='', type=str)
    city = request.args.get('city', default='', type=str)

    autoruPagesCount, dromPagesCount = '0', '0'

    brand = brand.replace(' ', '_', 1)
    if brand == 'ВАЗ_(LADA)':
        brand = 'vaz'
    if brand.lower()[0] in dic:
        brand = ''.join([dic[i] for i in brand.lower()])
    if brand == 'moskvich':
        brand = 'moscvich'
    if brand == 'Mercedes-Benz':
        brand = 'mercedes'
    if brand == 'SsangYong':
        brand = 'ssang_yong'
    brand = brand.lower()

    autoru_city = city
    if 'Республика' in autoru_city:
        for i in autoru_city.split():
            if 'Республика' not in i:
                autoru_city = i
    autoru_city = '_'.join(autoru_city.split(' '))
    autoru_city = ''.join([dic[i] for i in autoru_city.lower()])
    autoru = autoru_parse(brand, page, sort, autoru_city)
    # drom = drom_parse(brand, page, sort, region_dic[city])

    drom = []

    if autoru:
        autoru, autoruPagesCount = autoru
    if drom:
        drom, dromPagesCount = drom
    all_result = autoru + drom
    random.shuffle(all_result)
    if sort == 'По цене ↑':
        all_result.sort(key=lambda x: int(''.join(x['price'][:x['price'].index('₽')].split())))
    if sort == 'По цене ↓':
        all_result.sort(key=lambda x: int(''.join(x['price'][:x['price'].index('₽')].split())), reverse=True)
    # ---------------------------------------------------------------------------------------------------------------
    all_result.append((max(map(int, [autoruPagesCount, dromPagesCount])), brand, sort, city))
    # ---------------------------------------------------------------------------------------------------------------
    if len(all_result) > 1:
        return render_template('temp.html', cars=all_result)
    else:
        return render_template('temp.html', cars=[{
            'title': 'По вашему запросу ничего не найдено',
            'link': '',
            'photo': '',
            'year': '',
            'km': '',
            'motor': '',
            'price': ''
        }])


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
