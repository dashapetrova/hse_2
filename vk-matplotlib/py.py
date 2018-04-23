import urllib.request
import json
import re
import os

#https://vk.com/public43215063
token = 'af08b270af08b270af08b270e2af6af668aaf08af08b270f5cf0e82bc93152f8e2d356b'

req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-43215063&count=1&filter=all&v=5.74&access_token={}'.format(token))
response = urllib.request.urlopen(req)
result = response.read().decode('utf-8')
result = json.loads(result)
total_p = result['response']['count']

total_num = 10000 # скачаем 10000 постов, каждые 100 новый offset

#создаем массив offset
i = 0
num=100
offs = []
while i < num:
    o=i*100
    offs.append(o)
    i+=1

posts = [] #посты
ids = [] #id постов
comms = [] #комменты
ids_comms = [] #id комментов
len_p = [] #массив длин постов
len_c = [] #массив длин комментов

d = os.getcwd()
os.makedirs('vk_group')
nd = d+'\\vk_group'
os.chdir(nd)

#качаем посты и их id
for ofs in offs:
    req2 = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=-43215063&count=100&offset={}&filter=all&v=5.74&access_token={}'.format(ofs, token))
    response2 = urllib.request.urlopen(req2)
    result2 = response2.read().decode('utf-8')
    result2 = json.loads(result2)
    for j in range(100):        
        posts.append(result2['response']['items'][j]['text'])
        ids.append(result2['response']['items'][j]['id'])
        j += 1
        
name='posts.txt'
f = open(name, 'a', encoding = "utf-8")
for p in posts:
    f.write(p+'\n')
f.close()

#скачиваем комменты и id комментаторов
id_p = result['response']['items'][0]['id'] # id верхнего коммента
for  i, id_p in enumerate(ids):
    req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-43215063&post_id={}&count=1&v=5.74&access_token={}'.format(id_p, token))
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    result = json.loads(result)
    total = result['response']['count']
        offs_2 = []
    x = total//100
    i=0
    while i <= x:
        o=i*100
        offs.append(o)
        i+=1
    comms.append([])
    ids_comms.append([])
    for off in offs_2:
        req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=-43215063&post_id={}&offset={}&count=100&v=5.74&access_token={}'.format(id_p, off, token))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        result = json.loads(result)
        for comment in result['response']['items']:
            comms[i].append(comment['text'])
            ids_comms[i].append(comment['from_id'])
            
name='comments.txt'
f = open(name, 'a', encoding = "utf-8")
for c in comms:
    f.write(str(c)+'\n')
f.close()

#чистим посты и комменты и получаем их длины
i=0
while i < len(comms):
    num2 = 0
    summ = 0
    j=0
    while j < len(comms[i]):
        comms[i][j] = re.sub('[.,;:?!@#$%^&()_+=—]', '', comms[i][j])
        num2 += 1
        summ += len(comms[i][j])
        j+=1
    if num2 != 0:
        len_c.append(summ / num2)
    else:
        len_c.append(0)
    posts[i] = re.sub('[.,;:?!@#$%^&()_+=—]', '', posts[i])
    len_p.append(len(posts[i]))
    i+=1
    
#первый график
import matplotlib.pyplot as plt
plt.title('Соотношение длин постов и средних длин комментариев к ним')
plt.xlabel('Длина поста')
plt.ylabel('Средняя длина комментариев')

X = len_p
Y = len_c

plt.bar(X, Y, color='green')
plt.show()

#возраст и город пользователей
towns = []
ages = []
for i in range(len(ids)):
    req = urllib.request.Request('https://api.vk.com/method/users.get?user_ids={}&fields=bdate,city,home_town&v=5.73&access_token={}'.format(ids[i],token))
    response3 = urllib.request.urlopen(req)
    result3 = response3.read().decode('utf-8', errors = 'ignore')
    data = json.loads(result3)
    if re.search('bdate', result3):
        bdate = data['response'][0]['bdate']
        if re.search('\d+\.\d+.(\d+)', bdate):
            year = re.search('\d+\.\d+.(\d+)', bdate).group(1)
            age = 2018-int(year)
            ages.append(age)
        else:
            ages.append('')
    else:
        ages.append('')
    if re.search('home_town', result3):
        city = data['response'][0]['home_town']
        towns.append(city)
    else:
        if re.search('city', result3):
            city = data['response'][0]['city']['title']
            towns.append(city)
        else:
            towns.append('')


