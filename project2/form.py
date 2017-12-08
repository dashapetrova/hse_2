from flask import Flask
from flask import render_template, request
import json
import re

app = Flask(__name__)

@app.route('/')
def index():
    if request.args:
        name = request.args['name']
        lang = request.args['lang']
        gend = request.args['gend']
        age = request.args['age']
        im1 = request.args['im1']
        im2 = request.args['im2']
        im3 = request.args['im3']
        im4 = request.args['im4']
        im5 = request.args['im5']
        im6 = request.args['im6']
        im7 = request.args['im7']
        im8 = request.args['im8']
        d = {'name':name,'lang':lang,'gend':gend,'age':age,'im1':im1,'im2':im2,'im3':im3,'im4':im4,'im5':im5,'im6':im6,'im7':im7,'im8':im8}
        data = json.dumps(d)
        f2 = open('datas_2.json','a')
        f2.write(data+'\n')
        f2.close()
        return render_template('merci.html')
    return render_template('index.html')

@app.route('/stats')
def stats():
    i = 0
    sum1=0
    f = open('datas_2.json')
    for line in f.readlines():
        i+=1
    f.close()
    f = open('datas_2.json')
    text = f.read()
    sum1 = sum1+len(re.findall('"im1":',text))
    s1 = len(re.findall('"im1": "salut"',text))
    ns1 = s1*100/sum1
    nf1 = 100 - ns1

    s2 = len(re.findall('"im2": "salut"',text))
    ns2 = s2*100/sum1
    nf2 = 100 - ns2

    s3 = len(re.findall('"im3": "salut"',text))
    ns3 = s3*100/sum1
    nf3 = 100 - ns3

    s4 = len(re.findall('"im4": "salut"',text))
    ns4 = s4*100/sum1
    nf4 = 100 - ns4

    s5 = len(re.findall('"im5": "divan"',text))
    ns5 = s5*100/sum1
    nf5 = 100 - ns5

    s6 = len(re.findall('"im6": "divan"',text))
    ns6 = s6*100/sum1
    nf6 = 100 - ns6

    s7 = len(re.findall('"im7": "divan"',text))
    ns7 = s7*100/sum1
    nf7 = 100 - ns7

    s8 = len(re.findall('"im8": "divan"',text))
    ns8 = s8*100/sum1
    nf8 = 100 - ns8
    f.close()
    m = []
    f = open('datas_2.json')
    for line in f.readlines():
        line2 = eval(line)
        m.append(line2)
    f.close()
    nm1=nm2=nm3=nm4=nm5=nm6=nm7=nm8=mm1=mm2=mm3=mm4=mm5=mm6=mm7=mm8=0
    vse=0
    for j in m:
        vse+=1
        for k in j.items():
            if k == ('im1','salut'):
                for k in j.items():
                  if k == ('gend','m'):
                     nm1+=1
            if k == ('im2','salut'):
                for k in j.items():
                  if k == ('gend','m'):
                     nm2+=1
            if k == ('im3','salut'):
                for k in j.items():
                  if k == ('gend','m'):
                     nm3+=1
            if k == ('im4','salut'):
                for k in j.items():
                  if k == ('gend','m'):
                     nm4+=1
            if k == ('im5','divan'):
                for k in j.items():
                  if k == ('gend','m'):
                     nm5+=1
            if k == ('im6','divan'):
                for k in j.items():
                  if k == ('gend','m'):
                     nm6+=1
            if k == ('im7','divan'):
                for k in j.items():
                  if k == ('gend','m'):
                     nm7+=1
            if k == ('im8','divan'):
                for k in j.items():
                  if k == ('gend','m'):
                     nm8+=1
            if k == ('im1','fireworks'):
                for k in j.items():
                  if k == ('gend','m'):
                     mm1+=1
            if k == ('im2','fireworks'):
                for k in j.items():
                  if k == ('gend','m'):
                     mm2+=1
            if k == ('im3','fireworks'):
                for k in j.items():
                  if k == ('gend','m'):
                     mm3+=1
            if k == ('im4','fireworks'):
                for k in j.items():
                  if k == ('gend','m'):
                     mm4+=1
            if k == ('im5','kanape'):
                for k in j.items():
                  if k == ('gend','m'):
                     mm5+=1
            if k == ('im6','kanape'):
                for k in j.items():
                  if k == ('gend','m'):
                     mm6+=1
            if k == ('im7','kanape'):
                for k in j.items():
                  if k == ('gend','m'):
                     mm7+=1
            if k == ('im8','kanape'):
                for k in j.items():
                  if k == ('gend','m'):
                     mm8+=1
    nm1 = nm1*100/vse ; nw1 = 100 - nm1
    nm2 = nm2*100/vse;  nw2 = 100 - nm2
    nm3 = nm3*100/vse; nw3 = 100 - nm3
    nm4 = nm4*100/vse; nw4 = 100 - nm4
    nm5 = nm5*100/vse; nw5 = 100 - nm5
    nm6 = nm6*100/vse; nw6 = 100 - nm6
    nm7 = nm7*100/vse; nw7 = 100 - nm7
    nm8 = nm8*100/vse; nw8 = 100 - nm8
    
    mm1 = mm1*100/vse; mw1 = 100 - mm1
    mm2 = mm2*100/vse; mw2 = 100 - mm2
    mm3 = mm3*100/vse; mw3 = 100 - mm3
    mm4 = mm4*100/vse; mw4 = 100 - mm4
    mm5 = mm5*100/vse; mw5 = 100 - mm5
    mm6 = mm6*100/vse; mw6 = 100 - mm6
    mm7 = mm7*100/vse; mw7 = 100 - mm7
    mm8 = mm8*100/vse; mw8 = 100 - mm8
    return render_template('stats.html', vsego = i,ns1=ns1,nf1=nf1,ns2=ns2,nf2=nf2,ns3=ns3,nf3=nf3,
                           ns4=ns4,nf4=nf4,ns5=ns5,nf5=nf5,ns6=ns6,nf6=nf6,ns7=ns7,nf7=nf7,ns8=ns8,nf8=nf8,
                           nm1=nm1,nw1=nw1,nm2=nm2,nw2=nw2,nm3=nm3,nw3=nw3,nm4=nm4,nw4=nw4,nm5=nm5,nw5=nw5,
                           nm6=nm6,nw6=nw6,nm7=nm7,nw7=nw7,nm8=nm8,nw8=nw8,
                           mm1=mm1,mm2=mm2,mm3=mm3,mm4=mm4,mm5=mm5,mm6=mm6,mm7=mm7,mm8=mm8,
                           mw1=mw1,mw2=mw2,mw3=mw3,mw4=mw4,mw5=mw5,mw6=mw6,mw7=mw7,mw8=mw8,)

@app.route('/json')
def jsn():
    f = open('datas_2.json')
    text = f.read()
    return render_template('json.html', info = text)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/results')
def results():
    result = []
    answers_2 = []
    ques = request.args['search']
    with open('datas_2.json', "r") as file: 
        info = file.read()
    answers = info.split('}')
    for i in answers:
        j = re.sub(r'(\[|]|"|{)', '', i)
        answers_2.append(j)
    for j in answers_2:
        if re.search(ques, j):
            result.append(j)
    return render_template('results.html', result = result) 

if __name__ == '__main__':
    app.run(debug=True)
