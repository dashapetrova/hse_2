import urllib.request
import re
import os
import json
from flask import Flask
from flask import render_template, request

app = Flask(__name__)

def getdic():
    d={}
    site = 'file:///C:/Python33/thai_pages/'
    fs = os.listdir('thai_pages')
    for i in range(0,len(fs)):
        link = site+fs[i]
        req = urllib.request.Request(link)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        s="<tr><td class=th><a href='/id/.*?'>(.*?)</a></td><td>.*?<span class='.*?'>.*?</span>.*?<span class='.*?'>.*?</span>.*?<span class='.*?'>.*?</span>.*?<span class='.*?'>.*?</span></td><td class=.*?>.*?</td><td>(.*?)</td></tr>"
        rewords = re.compile(s, re.DOTALL)
        reTag = re.compile('<.*?>',re.DOTALL)
        words = rewords.findall(html)
        for i in range(0,len(words)):
            d[words[i][0]]=words[i][1]
    return d

def d2():
    d1 = getdic()
    d2 = {}
    for k in d1:
        k2 = d1[k]
        v2 = k
        d2[k2]=v2
    return d2

def json():
    d = getdic()
    json_string = json.dumps(d)
    with open('dict1.json', "w", newline="") as file:
        print(json_string)
        
def json2():
    d1 = getdic()
    d2 = {}
    for k in d1:
        k2 = d1[k]
        v2 = k
        d2[k2]=v2
    json_string = json.dumps(d2)
    with open('dict2.json', "w", newline="") as file:
        print(json_string)

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/result')
def index_2():
    d = d2()
    ans_word=''
    word = request.args['word']
    for key in d:
        if word == key:
            ans_word = d[key]
    if ans_word == '':
        ans_word = 'Совпадений не найдено.'
    return render_template('result.html', word = ans_word)

if __name__ == '__main__':
    app.run(debug=True)
