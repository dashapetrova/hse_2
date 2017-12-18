import urllib.request 
import re
import matplotlib.pyplot as plt


def link:
    req = urllib.request.Request('http://wiki.dothraki.org/Vocabulary')
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    return html

def letters:
    html = link()
    lets = {}
    reLetter = re.compile('<span class="mw-headline" id="(\w)">(.*?)</span></h3>(.*?)<h3>', re.DOTALL)
    #рассмотрим Z отдельно, чтобы не захватить лишнего, т.к. у Futher Information тег не h3, h2
    reZ = re.compile('<span class="mw-headline" id="Z">(.*?)</span></h3>(.*?)<h2>', re.DOTALL)
    reword = re.compile('<span id="(.*?)">', re.DOTALL)
    for i in re.findall(reLetter, html):
        lets[i[0]]= '0'
        for j in re.findall(reword, i[2]):
            let[i[0]] = str(int(lets[i[0]]) + 1)
    lets['Z']= '0'
    for i in re.findall(reZ, html):
        for j in re.findall(reword, i[1]):
            let['Z'] = str(int(lets['Z']) + 1)
    return lets

def num_parts():
    names = ['nouns', 'proper nouns', 'pronouns', 'verbs','adjectives', 'adverbs',
             'numerals','prepositions', 'conjunctions', 'determiners', 'interjections']
    parts = {}
    for n in names:
        parts[n]='0'
    html = link()
    rep = re.compile('<ul><li><b>(\w*?)</b>(.*?)(<dd><i>(.*?)</i>(\w*?)</dd>)*</dl>', re.DOTALL)
    regp = re.compile('<i>(.*?)</i>', re.DOTALL)
    words = re.findall(rep, html)
    for i in words:
        for j in re.findall(regp, i[1]):
            if j == 'ni.' or j == 'na.' or j == 'n.' or j == 'np.':
                n1 = int(parts['nouns']) + 1
                parts['nouns'] = str(n1)
            if j == 'prop. n.':
                n2 = int(parts['proper nouns']) + 1
                parts['proper nouns'] = str(n2)
            if j == 'pn.':
                n3 = int(parts['pronouns']) + 1
                parts['pronouns'] = str(n3)
            if j == 'v. aux.' or j == 'v.' or j == 'vin.' or j == 'vtr.':
                n4 = int(parts['verbs']) + 1
                parts['verbs'] = str(n4)
            if j == 'adj.':
                n5 = int(parts['adjectives']) + 1
                parts['adjectives'] = str(n5)
            if j == 'adv.':
                n6 = int(parts['adverbs']) + 1
                parts['adverbs'] = str(n6)
            if j == 'num.':
                n7 = int(parts['numerals']) + 1
                parts['numerals'] = str(n7)
            if j == 'prep.':
                n8 = int(parts['prepositions']) + 1
                parts['prepositions'] = str(n8)
            if j == 'conj.':
                n9 = int(parts['conjunctions']) + 1
                parts['conjunctions'] = str(n9)
            if j == 'det.':
                n10 = int(parts['determiners']) + 1
                parts['determiners'] = str(n10)
            if j == 'intj.':
                n11 = int(parts['interjections']) + 1
                parts['interjections'] = str(n11)  
    return parts

def main():
    lets = letters()
    parts = num_parts()
    lets_2 = []
    let_num = []
    parts_2 = []
    part_num = []
    for i in lets:
        lets_2.append(i) 
        let_num.append(int(lets[i]))
    for j in parts:
        parts_2.append(k) 
        part_num.append(int(parts[k]))
        
    Xl = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    Xp = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    Yl = let_num
    Yp = part_num

    plt.xticks(Xl, lets_2)
    plt.bar(Xl, Yl, color='green')
    plt.title("Число слов для каждой буквы дотракийского алфавита")
    plt.show()

    plt.xticks(Xp, parts_2)
    plt.bar(Xp, Yp, color='blue')
    plt.title("Число слов каждой части речи")
    plt.show()

if __name__ == '__main__':
    main()
