from flask import Flask, request, render_template, make_response
from parse import *
import random

app = Flask(__name__)
dic = {'Ь':'', 'ь':'', 'Ъ':'', 'ъ':'', 'А':'A', 'а':'a', 'Б':'B', 'б':'b', 'В':'V', 'в':'v',
       'Г':'G', 'г':'g', 'Д':'D', 'д':'d', 'Е':'E', 'е':'e', 'Ё':'Yo', 'ё':'yo', 'Ж':'Zh', 'ж':'g',
       'З':'Z', 'з':'z', 'И':'I', 'и':'i', 'Й':'Y', 'й':'y', 'К':'K', 'к':'k', 'Л':'L', 'л':'l',
       'М':'M', 'м':'m', 'Н':'N', 'н':'n', 'О':'O', 'о':'o', 'П':'P', 'п':'p', 'Р':'R', 'р':'r',
       'С':'S', 'с':'s', 'Т':'T', 'т':'t', 'У':'U', 'у':'u', 'Ф':'F', 'ф':'f', 'Х':'H', 'х':'h',
       'Ц':'Ts', 'ц':'ts', 'Ч':'Ch', 'ч':'ch', 'Ш':'Sh', 'ш':'sh', 'Щ':'Sch', 'щ':'sch', 'Ы':'Yi',
       'ы':'yi', 'Э':'E', 'э':'e', 'Ю':'Yu', 'ю':'yu', 'Я':'Ya', 'я':'ya', '_': '_', '-': '-'}


def drom_city(city):
    r_wik = requests.get('https://ru.wikipedia.org/wiki/Коды_субъектов_Российской_Федерации')
    soup_wik = BeautifulSoup(r_wik.text, 'html.parser')

    if city == 'Республика Крым':
        return '82'
    for j in soup_wik.find_all('tr')[1:]:
        if j.select_one('td'):
            if j.select_one('td').text == city:
                return str(int(j.select('td')[2].text.split(', ')[0]))


@app.route('/cars')
def get():
    page = request.args.get('page', default='1', type=str)
    t = request.args.get('marka', default='', type=str)
    sor = request.args.get('sort', default='', type=str)
    city = request.args.get('city', default='', type=str)
    print(city)

    autoru_pg, drom_pg = '0', '0'


    t = t.replace(' ', '_')
    if t == 'ВАЗ_(LADA)':
        t = 'vaz'
    if t.lower()[0] in dic:
        t = ''.join([dic[i] for i in t.lower()])
    if t == 'moskvich':
        t = 'moscvich'
    if t == 'Mercedes-Benz':
        t = 'mercedes'
    if t == 'SsangYong':
        t = 'ssang_yong'
    t = t.lower()

    autoru_city = city
    if 'Республика' in city:
        for i in autoru_city.split():
            if 'Республика' not in i:
                autoru_city = i
    autoru_city = '_'.join(autoru_city.split(' '))
    autoru_city = ''.join([dic[i] for i in autoru_city.lower()])
    autoru = autoru_parse(t, page, sor, autoru_city)
    drom = drom_parse(t, page, sor, drom_city(city))
    if autoru:
        autoru, autoru_pg = autoru
    if drom:
        drom, drom_pg = drom
    all_result = autoru + drom
    random.shuffle(all_result)
    if sor == 'По цене ↑':
        all_result.sort(key=lambda x: int(''.join(x['price'][:x['price'].index('₽')].split())))
    if sor == 'По цене ↓':
        all_result.sort(key=lambda x: int(''.join(x['price'][:x['price'].index('₽')].split())), reverse=True)
    # ---------------------------------------------------------------------------------------------------------------
    all_result.append((max(map(int, [autoru_pg, drom_pg])), t, sor))
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