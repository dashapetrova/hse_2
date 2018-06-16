#Веб-сервис: получает от пользователя юзернейм в твиттере,
#скачивает твиты этого пользователя,
#строит график частотности хэштегов в течение времени существования аккаунта
import tweepy
from credentials import *
import re
import matplotlib
import matplotlib.pyplot as plt
from flask import Flask
from flask import render_template, request
import time

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

app = Flask(__name__)

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)
            
@app.route('/')
def index():
    if request.args:
        username = request.args['username']
        user = api.get_user(username)
        hashtags = []
        for tweet in limit_handled(tweepy.Cursor(api.user_timeline, screen_name=username).items()):
            str_tw = tweet.text
            str_tw = re.sub(r"[^A-Za-zА-Яа-я#\s]+", '', str_tw)
            rehash = re.compile('#.*? ', flags= re.DOTALL)
            tags = rehash.findall(tweet.text)
            for i in tags:
                i = re.sub(r"[^A-Za-zА-Яа-я#\s]+", '', i)
                i = i.split()
                resh = '#'
                for j in i:
                    if resh in j:
                        hashtags.append(j)
        d = {} #словарь частотности хэштегов
        for h in hashtags:
            if h in d.keys():
                d[h]+=1
            else:
               d[h]=1
        x = []
        y = []
        for i in d.keys():
            x.append(i)
        for j in d.values():
            y.append(j)
        plt.xlabel('hashtag')
        plt.ylabel('frequency')
        plt.xticks(rotation=90)
        plt.tick_params(axis='x', which='major', labelsize=6)
        plt.bar(x, y, color='g')
        plt.savefig('static/freq.png')
        return render_template('graph.html', name = username)
    return render_template('index.html')

if __name__ == '__main__':
   app.run(debug = True)
