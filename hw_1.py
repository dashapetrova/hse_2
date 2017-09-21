import urllib.request
import re

req = urllib.request.Request('http://pav-edin23.ru/category/obrazovanie/')
with urllib.request.urlopen(req) as response:
   html = response.read().decode('utf-8')

regPostTitle = re.compile('<h2 class="entry-title">.*?</h2>', flags= re.DOTALL)
titles = regPostTitle.findall(html)

new_titles = []
regTag = re.compile('<.*?>', re.DOTALL)
regSpace = re.compile('\s{2,}', re.DOTALL)
for t in titles:
    clean_t = regSpace.sub("", t)
    clean_t = regTag.sub("", clean_t)
    new_titles.append(clean_t)
    
f = open('result.txt', 'w', encoding = "utf-8")
for i in range(len(new_titles)):
    f.write(new_titles[i]+'\n')
f.close()
