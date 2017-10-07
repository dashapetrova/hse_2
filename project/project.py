import urllib.request
import re
import os
import time

d = os.getcwd()
os.makedirs('newspaper')
nd = d+'\\newspaper'
os.chdir(nd)

def download_page(pageUrl):
    try:
        time.sleep(1)
        page = urllib.request.urlopen(pageUrl)
        text = page.read().decode('UTF-8')
        regPostTitle = re.compile('<a class="meta-more" href="(.*?)">Читать далее <span class="meta-nav">&raquo;</span></a>', flags= re.DOTALL)
        titles = regPostTitle.findall(text)
        new = [] #массив ссылок статей
        
        clear1 = re.compile('<a class="meta-more" href="', re.DOTALL)
        clear2 = re.compile('">Читать далее <span class="meta-nav">&raquo;</span></a>', re.DOTALL)
        for t in titles:
            clean_t = clear1.sub("", t)
            clean_t = clear2.sub("", clean_t)
            new.append(clean_t)
        return new
    except:
        print('Error at', pageUrl)
        return
def download_post(link):
    req = urllib.request.Request(link)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
    regPostText = re.compile('<p>.*?</p>', flags= re.DOTALL)
    texts = regPostText.findall(html)
    posts = []
    
    regTag = re.compile('<.*?>', re.DOTALL)
    regSpace = re.compile('\s{2,}', re.DOTALL)
    clear3 = re.compile('&nbsp;', re.DOTALL)
    clear4 = re.compile('&#8211;', re.DOTALL)
    for t in texts:
        clean_t = regSpace.sub("", t)
        clean_t = regTag.sub("", clean_t)
        clean_t = clear3.sub("", clean_t)
        clean_t = clear4.sub("–", clean_t)
        posts.append(clean_t)
    return posts
def meta(link):
    req = urllib.request.Request(link)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
    regPostDate = re.compile('<span class="meta-date">.*?</span>', flags= re.DOTALL)
    date = regPostDate.findall(html)
    regPostCat = re.compile('rel="category tag">.*?</a></span>', flags= re.DOTALL)
    cat = regPostCat.findall(html)
    m=[]
    regTag = re.compile('<.*?>', re.DOTALL)
    regSpace = re.compile('\s{2,}', re.DOTALL)
    regClear = re.compile('rel="category tag">', re.DOTALL)
    regPostTitle = re.compile('<h1 class="entry-title">.*?</h1>', flags= re.DOTALL)
    regClear2 = re.compile('&#8211;', re.DOTALL)
    titles = regPostTitle.findall(html)
    author = "NoName" #авторы не указаны
    m.append(author)
    for t in titles:
        clean_1 = regSpace.sub("", t)
        clean_1 = regTag.sub("", clean_1)
        clean_1 = regClear2.sub("–", clean_1)
        m.append(clean_1)
    for d in date:
        clean_2 = regSpace.sub("", d)
        clean_2 = regTag.sub("", clean_2)
        m.append(clean_2) 
    for c in cat:
        clean_3 = regSpace.sub("", c)
        clean_3 = regTag.sub("", clean_3)
        clean_3 = regClear.sub("",clean_3)
        m.append(clean_3)
    return m

commonUrl = 'http://pav-edin23.ru/'
num = 1
suum = 0
os.makedirs('plain')
os.makedirs('mystem-plain')
os.makedirs('mystem-xml')
nd_2 = nd + '\\plain'
nd_4 = nd + '\\mystem-plain'
nd_6 = nd + '\\mystem-xml'
meta_data = []
for g in range(2017,2018):
    os.chdir(nd_2); os.makedirs(str(g))
    os.chdir(nd_4); os.makedirs(str(g))
    os.chdir(nd_6); os.makedirs(str(g))
    nd_3 = nd_2+'\\'+str(g)
    for i in range(1,5):
        os.chdir(nd_3)
        os.makedirs(str(i))
        os.chdir(nd_4 + '\\' + str(g)); os.makedirs(str(i))
        os.chdir(nd_6 + '\\' +str(g)); os.makedirs(str(i))
        os.chdir(nd_3+'\\'+str(i))
        if i < 10:
            pageUrl = commonUrl + str(g) + '/0'+str(i) +'/'
        else:
            pageUrl = commonUrl + str(g) + '/'+str(i) +'/'
        m = download_page(pageUrl) #массив ссылок статей
        for j in m:
            met = meta(j)
            posts = download_post(j) # массив параграфов на одной странице
            name_0 = 'article_' + str(num)
            name = name_0 + '.txt'
            f = open(name, 'a', encoding = "utf-8")
            for p in range(len(posts)): #записываем параграфы в пост
                f.write(posts[p]+'\n')
                suum = suum + len(posts[p])
            f.close()
            path = os.getcwd()
            os.chdir(d)
            input_txt = os.path.join('newspaper', 'plain', str(g), str(i), name_0 + '.txt ')
            output_txt = os.path.join('newspaper', 'mystem-plain', str(g), str(i), name_0 + '.txt')
            os.system('mystem.exe ' + '-di ' + input_txt + output_txt)
            output_xml = os.path.join('newspaper', 'mystem-xml', str(g), str(i), name_0 + '.xml')
            os.system('mystem.exe ' + '-di ' + input_txt + output_xml)
            met.insert(0,path)
            met.append(j)
            met.append(str(g))
            meta_data.append(met)
            os.chdir(nd_3+'\\'+str(i))
            bu = open(name,'r',encoding='utf-8')
            t = bu.read()
            bu.close()
            w = open(name,'w',encoding = 'utf-8')
            w.write('@au ' + met[0] + '\n')
            w.close()
            dop = open(name,'a',encoding = 'utf-8')
            dop.write('@ti ' + met[1] + '\n')
            dop.write('@da' + met[2] + '\n')
            dop.write('@topic ' + met[3] + '\n')
            dop.write('@url ' + j + '\n'+'\n')
            dop.write(t)
            dop.close()
            num += 1
            os.chdir(nd_3+'\\'+str(i))
    os.chdir(nd)
print(suum)
def csv_write(massive): # записываем мета данные в файл
    data = massive
    with open("meta_data.csv", "a", encoding = 'utf-8') as file:
        file.write('path\tauthor\tsex\tbirthday\theader\tcreated\tsphere\tgenre_f\ttype\ttopic\tchronotop\tstyle\taudience_age\taudience_level\taudience_size\tsource\tpublication\tpublisher\tpubl_year\tmedium\tcountry\tregion\tlanguage')
        for i in range(len(data)):
            mas = data[i]
            row = mas[0]+'\t'+mas[1]+'\t\t\t'+mas[2]+'\t'+mas[3]+'\tпублицистика\t\t\t'+mas[4]+'\t\tнейтральный\tн-возраст\tн-уровень\tрайонная(если районная)\t'+mas[5]+'\tназвание газеты\t\t'+mas[6]+'\tгазета\tРоссия\tкакой-то регион\tru\n'
            file.write(row)
csv_write(meta_data)
