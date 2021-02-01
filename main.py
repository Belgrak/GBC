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
       'ы':'yi', 'Э':'E', 'э':'e', 'Ю':'Yu', 'ю':'yu', 'Я':'Ya', 'я':'ya'}


@app.route('/cars')
def get():
    page = request.args.get('page', default='1', type=str)
    t = request.args.get('marka', default='', type=str)
    t = t.replace(' ', '_')
    if t == 'ВАЗ_(LADA)':
        t = 'vaz'
    if t.lower()[0] in dic:
        t = ''.join([dic[i] for i in t.lower()])
    if t == 'moskvich':
        t = 'moscvich'
    if t == 'Mercedes-Benz':
        t = 'mercedes'
    t = t.lower()
    autoru, autoru_pg = autoru_parse(t, page)
    drom, drom_pg = drom_parse(t, page)
    all_result = autoru + drom
    random.shuffle(all_result)
    all_result.append((max(map(int, [autoru_pg, drom_pg])), t))
    if all_result:
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


if __name__ == '__main__':
    app.run()