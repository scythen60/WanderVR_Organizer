import requests
import re
import sqlite3
import time
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import wanderclean

def svf3():
    con = sqlite3.connect('wander.db')
    cur = con.cursor()     
    cur.execute("select count(*) from svf_pages where panoid like '%2F%' and panoid like '-%' and length(panoid)>22;")
    end = cur.fetchone()[0]
	# ADD KEY HERE
    converturl = "https://maps.googleapis.com/maps/api/streetview/metadata?key=ADD KEY HERE&pano="
    for i in range(0,end):
        cur.execute("select panoid, post_id from svf_pages where panoid like '%2F%' and panoid like '-%' and length(panoid)>22 LIMIT 1;")
        pano = cur.fetchone()
        post_id = pano[1]
        panoid = pano[0]
        print(panoid)
        panoid = panoid.replace("%2F", "/")
        panoid='F:'+panoid
        print(converturl+panoid)
        response = requests.get(converturl+panoid)
        panoid = response.json().get('pano_id')
        
        if panoid:
            print('KEEP successful conversion to ' + panoid)
            cur.execute("update svf_pages set panoid = ? where post_id = ?;",[panoid,post_id])
        else: 
            print('DEL failed conversion')
            cur.execute("update svf_pages set panoid = 'BAD' where post_id = ?;",[post_id])
        con.commit()
    cur.execute("insert or ignore into pano(panoid) select a.panoid from svf_pages a left join pano b on a.panoid=b.panoid where length(a.panoid)>20 and b.panoid is null;")
    con.commit()
    wanderclean.getlatlng22()
    wanderclean.getlatlng44()
    return
    
def svf2():
    con = sqlite3.connect('wander.db')
    cur = con.cursor()     
    cur.execute("select count(*) from svf_pages where panoid ='' and map_url like '%goo.gl%';")
    end = cur.fetchone()[0]
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    if end != None and end >= 1:
        driver = webdriver.Chrome(options=chrome_options, executable_path='chromedriver')  # Optional argument, if not specified will search path.
        for i in range(0,end):
            print('records left: ' + str(end-i))       
            pano = cur.execute("select map_url, post_id from svf_pages where panoid ='' and map_url like '%goo.gl%' LIMIT 1;")
            pano = cur.fetchone()
            post_id = pano[1]
            url = pano[0]
            driver.get(url);
            theurl = driver.current_url
            print(theurl)
            n=0
            while '!2e' not in theurl:
                n+=1
                time.sleep(1)
                theurl = driver.current_url
                if n == 10:
                    break
            match = re.findall(r'!1s(.*)!2e', theurl)
            panoid = ''
            for i in match:
                panoid = i
            if '!2e' in panoid:
                panoid = panoid.split('!2e')[0]
            if 'panoid' in theurl and panoid == '':
                panoid = panoid.split('panoid=')
                if '&' in panoid:
                    panoid = panoid[1].split('&')[0]
            
            if panoid == '':
                panoid = 'NONE'
            print(panoid, '|' , post_id)
            
            cur.execute("update svf_pages set panoid = ? where post_id = ?;",[panoid,post_id])
            con.commit()
    con.close()  
    return
    
def svf():
    con = sqlite3.connect('wander.db')
    cur = con.cursor()    
    for i in range(1,2):
        print(i)
        r = requests.get('https://www.streetviewfun.com/page/'+str(i))
        soupData = BeautifulSoup(r.text,features="lxml")
        for a in soupData.find_all('article'):
            title = ''
            map_url = ''
            panoid = ''
            post_id = ''
            tags = []
            svf_url = ''
            published = ''
            #article title
            title = a.find('h2', {'class':'entry-title'}).text
            #article id
            post_id = a['class'][0].split('-')[1]
            #categories and tags
            for i in a['class']:
                if 'category-' in i or 'tag-' in i:
                    tags.append(i)
            #post's direct link
            for i in a.find_all('a', href=True):
                svf_url = i['href']
                break
            #published datetime    
            for i in a.find_all('time', {'class':'entry-date published'}):
                time = i['datetime']
                time = time.split('T')
                d = datetime.strptime(time[1].split('-')[0], "%H:%M:%S")
                published=time[0] + ' at ' + d.strftime("%#I:%M %p")
            #Find Map URL last href or embedded 
            for i in a.find_all('div', {'class':'entry-content'}):
                for c in i.find_all('a', href=True):
                    if 'maps' in c['href']:
                        map_url=(c['href'])
            if map_url == None:
                for m in a.find_all('iframe', src=True):
                    map_url=(m['src']) 
            #panoid
            match = re.findall(r'!1s(.*)!2e', map_url)
            for i in match:
                panoid = i
            if '!2e' in panoid:
                panoid = panoid.split('!2e')[0]
            if 'panoid' in map_url and panoid == '':
                panoid = panoid.split('panoid=')
                if '&' in panoid:
                    panoid = panoid[1].split('&')[0]

            print(title, '|', panoid, '|', published, '|', svf_url, '|', map_url, '|', tags, '|', post_id)
            cur.execute("INSERT OR IGNORE INTO svf_pages (panoid, published, title, svf_url, map_url, tags, post_id) VALUES (?, ?, ?, ?, ?, ?, ?);",[panoid, published, title, svf_url, map_url, str(tags), post_id])
            con.commit()
    con.close()
    svf2()
    svf3()

def funnystash():
    return

def bm():
    n=0
    fr = open('tmp.txt','r',encoding='utf-8')
    f = open('output.txt','w',encoding='utf-8')

    for i in fr:
        match = re.findall(r'!1s(.*?)!2', i)
        for i in match:
            print(i)
            f.write(i+'\n')
            n+=1
        match2 = re.findall(r'/p/(.*?)=w600', i)
        for j in match2:
            print(j)
            f.write(j+'\n')
            n+=1
    f.close()
    print(n)
    
def har():
    n=0
    fr = open('tmp.txt','r',encoding='utf-8')
    f = open('output.txt','w',encoding='utf-8')

    for i in fr:
        if 'ro0-fo100' in i:
            # print(n)
            match2 = re.findall(r'/p/(.*?)=w600', i)
            for j in match2:
                if len(j)<100:
                    print(j)
                    f.write(j+'\n')
                    n+=1
    f.close()
    print(n)
    if n == 0:
      print('switching to bookmark parsing mode')
      bm()
    
def insertdb():
    con = sqlite3.connect('wander.db')
    cur = con.cursor()
    
    f = open('output.txt','r',encoding='utf-8')
    chunk = []
    # n=0
    for i in f:
        i = i.strip()
        # print(i)
        chunk.append([i])
    cur.executemany("INSERT OR IGNORE INTO pano (panoid) VALUES (?);",chunk)
    con.commit()
    print('Done inserting into DB, starting data append...')
    con.close()
    f.close()
    wanderclean.getlatlng22()
    wanderclean.getlatlng44()

if __name__ == "__main__":
    har()
    insertdb()

