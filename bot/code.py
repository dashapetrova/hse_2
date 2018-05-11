import telebot
import conf
from pymystem3 import Mystem
import pymorphy2
import re
import random
from pymorphy2 import MorphAnalyzer
import urllib.request  
import flask

morph = MorphAnalyzer()
m = Mystem()

f = open('textic.txt','r',encoding='utf-8')
text = f.read()
lemmas = m.lemmatize(text)

d={}
ana = m.analyze(text)
for i in ana:
    for k in i.keys():
        if k == 'analysis':
            for i in i[k]:
                gram = i['gr']
                reg1 = re.compile("(,|=).*",flags=re.DOTALL)
                new_gram = reg1.sub("",gram)
                lex = i['lex']
                d[lex]=new_gram
#d - словарь вида [word]:[part of speech]
#dic - словарь вида [part of speech]:[massive of word]
dic = {}
for k in d.keys():
    if d[k] in dic.keys():
        l = list(dic[d[k]])
        l.append(k)
        dic[d[k]]=str(l)
    else:
        dic[d[k]]=k

def rand(utext,dic):
    stuff = '[\.\?!"@№;%:?*_()-+=#$^&:;\'"><,/\|\\~`]'
    utext = re.sub(stuff, '', utext)
    string = ''
    for i in utext.split():
        j = 0
        ana = morph.parse(i)
        f_one = ana[0]
        tag1 = f_one.tag
        tag2 = f_one.normalized.tag
        for k in dic.keys():
            if k == tag2:
                i = random.choice(list(dic[k]))
        string = string + i
    return string

WEBHOOK_URL_BASE = "https://dashapetrova.pythonanywhere.com:433"
WEBHOOK_URL_PATH= "/{}/".format(conf.TOKEN)
url = WEBHOOK_URL_BASE + WEBHOOK_URL_PATH 

bot = telebot.TeleBot(conf.TOKEN)
bot.remove_webhook()
bot.set_webhook(url)

app = flask.Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user = message.chat.id
    bot.send_message(message.chat.id, "Здравствуйте! Это бот с большой фантазией. Напишите мне)")

@bot.message_handler(content_types=['text'])
def send_len(message):
    user = message.chat.id
    
    utext = message.text
    string = rand()
    bot.send_message(message.chat.id, string)

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

bot.polling(none_stop=True)

