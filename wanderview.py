import json,re,sqlite3
# import io
from collections import OrderedDict

# data = open('fav_output.txt','r')
url22 = 'https://maps.google.com/cbk?output=thumbnail&w=600&h=400&panoid='
url22b = 'https://maps.google.com/maps?q=ie=UTF8&layer=c&panoid='
url44a = 'https://lh5.googleusercontent.com/p/'
url44b = '=w600-h400-p-k-no-pi0-ya69.999985-ro0-fo100'

url1 = 'https://www.google.com/maps/@0,0,0a,0y,0h,0t/data=!3m11!1e1!3m9!1s'
url2 = '!2e10!3e11!6shttps:%2F%2Flh5.googleusercontent.com%2Fp%2F'
url3 = '%3Dw203-h100-k-no-pi2.6336086-ya5.846676-ro1.5802011-fo100!7i7776!8i3888!9m2!1b1!2i27'

# with open('Wander_favorites.json', 'r',encoding='utf-8') as file:
    # filedata = file.read() 
# match = re.findall(r'"panoid":"(.*?)"', filedata)
# data = []
# for i in match:
    # print(i)
    # data.append(i)
    
con = sqlite3.connect('wander.db')
cur = con.cursor()
cur.execute('select panoid from pano where timestamp > date("now", "-2 day") and panoid_verified = "OK" order by timestamp desc limit 4000;')
data = cur.fetchall()
con.close()

f=open("wander.html","w", encoding='utf-8')

for i in data:
    i = i[0]
    print(i)
    f.write('<a href="')
    if i[:2]=='AF' and len(i)>40:
        f.write(url1+i+url2+i+url3)
    elif len(i)==22:
        f.write(url22b+i)
    f.write('"><img src="')
    if i[:2]=='AF':
        f.write(url44a + i + url44b)
    elif len(i)==22:
        f.write(url22+i)
    f.write('" width="450" height="300"></a>')
    
f.close()

