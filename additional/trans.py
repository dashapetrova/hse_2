from flask import Flask
from flask import render_template, request
import urllib.request
import re
import os
import requests

app = Flask(__name__)

def getdic():
    d = {}
    site = 'http://www.dorev.ru/ru-index.html?l='
    alfa = ['c0', 'c1', 'c2','c3','c4','c5','c6', 'c7','c8','c9', 'ca','cb','cc','cd','ce','cf','d0','d1','d2','d3','d4','d5','d6','d7','d8','d9','dd','de','df']
    rewords = re.compile('<td class="uu">([А-Яа-я]*?)</td><td></td><td class="uu">(.*?)</td>', re.DOTALL)
    reone = re.compile('(([А-Яа-я]|\'|&#(\d{4});)*?)(,|\s|\b)', re.DOTALL)
    reTag = re.compile('<.*?>', re.DOTALL)
    for i in range(0, len(alfa)): 
        link = site + alfa[i]
        req = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)' })
        req.encoding = 'windows-1251'
        lets = req.text
        for i in re.findall(rewords, lets):
            d[i[0]] = reTag.sub("", i[1])
            if re.search(reone, d[i[0]]):
                d[i[0]] = re.search(reone, d[i[0]]).group(1)
    return d
        
def page():
    req = urllib.request.Request('https://lenta.ru/')
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
       
    r = '[а-яА-Я]+'
    m = re.findall(r,html)

    f = open('words.txt', 'a',encoding='utf-8')
    for i in m:
        f.write(i+' ')
    f.close()
    
    input_txt = os.path.join('words.txt ')
    output_txt = os.path.join('mys_words.txt')
    os.system('mystem.exe ' + '-l ' + input_txt + output_txt)
    
@app.route('/')
def index():
    req = urllib.request.Request('https://world-weather.ru/pogoda/macedonia/skopje/')
    with urllib.request.urlopen(req) as response:
       html = response.read().decode('utf-8')

    rPW = re.compile('<div id="weather-now-number">.*?<span>°C</span>', flags = re.DOTALL)
    temp = rPW.findall(html)
    regTag = re.compile('<.*?>', re.DOTALL)
    for t in temp:
        clean_t = regTag.sub(" ", t)

    return render_template('boot1.html',temp=clean_t)

@app.route('/boot5')
def index_2():
    d = getdic()
    ans_word=''
    word = request.args['word']
    for key in d:
        if word == key:
            ans_word = d[key]
    if ans_word == '':
        ans_word = 'Совпадений не найдено.'
    return render_template('boot5.html', word = ans_word) 
    
@app.route('/boot2')
def jsn():
    d = getdic()
    m = []
    output_txt = os.path.join('mys_words.txt')
    with open(output_txt, "r", encoding = 'utf-8') as file: 
        words = file.read()
    for w in words:
        for key in d:
            if w == key:
                j = d[key]
                m.append(j)
    return render_template('boot2.html',info = m)

@app.route('/boot3')
def site():
    return render_template('boot3.html')

@app.route('/boot4')
def site_2():
    corr = 0
    ans = dict(request.args)
    for i in ans:
        if ans[i][0] == 'r':
            corr += 1
    result = corr
    return render_template('boot4.html',result = result)

if __name__ == '__main__':
    page()
    app.run(debug=True)
