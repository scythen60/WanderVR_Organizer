import requests
import sys
import sqlite3
import reverse_geocoder as rg 
import time, re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def filldb():
    con = sqlite3.connect('wander.db')
    con.execute("PRAGMA journal_mode=WAL")
    cur = con.cursor()
    cur.execute("update pano set copyright = substr(copyright,3,length(copyright)) where copyright like '©%';")
    con.commit()
    cur.execute("update pano set title = cc||'|'||b.title from (SELECT title, panoid FROM svf_pages) AS b WHERE pano.panoid = b.panoid and pano.panoid_verified='OK' and pano.title is null;")
    con.commit()
    cur.execute("update pano set title = cc||'|'||admin1||'|'||name where panoid_verified='OK' and name!=admin1 and admin1!='' and copyright='Google' and description is null and title is null;")
    cur.execute("update pano set title = cc||'|'||name where panoid_verified='OK' and admin1='' and copyright='Google' and description is null and title is null; ")
    cur.execute("update pano set title = cc||'|'||name where panoid_verified='OK' and name=admin1 and copyright='Google' and description is null and title is null;")
    cur.execute("update pano set title = cc||'|'||admin1||'|'||name||'*' where panoid_verified='OK' and name!=admin1 and admin1!='' and copyright!='Google' and (description is null or description='') and title is null;")
    cur.execute("update pano set title = cc||'|'||name||'*' where panoid_verified='OK' and name = admin1 and copyright!='Google' and (description is null or description='') and title is null;")
    cur.execute("update pano set title = cc||'|'||name||'*' where panoid_verified='OK' and name is not null and admin1='' and copyright!='Google' and (description is null or description='') and title is null;")
    cur.execute("update pano set title = cc||'|'||admin1||'|'||name||'*'||'|'||description where panoid_verified='OK' and name!=admin1 and admin1!='' and copyright!='Google' and length(description)>1 and title is null;")
    cur.execute("update pano set title = cc||'|'||name||'*'||'|'||description where panoid_verified='OK' and name = admin1 and copyright!='Google' and length(description)>1 and title is null;")
    cur.execute("update pano set title = cc||'|'||name||'*'||'|'||description where panoid_verified='OK' and name is not null and admin1='' and copyright!='Google' and length(description)>1 and title is null; ")
    cur.execute("update pano set date = substr(date,5,length(date))||'-01' where date like 'Jan %';")
    cur.execute("update pano set date = substr(date,5,length(date))||'-02' where date like 'Feb %';")
    cur.execute("update pano set date = substr(date,5,length(date))||'-03' where date like 'Mar %';")
    cur.execute("update pano set date = substr(date,5,length(date))||'-04' where date like 'Apr %';")
    cur.execute("update pano set date = substr(date,5,length(date))||'-05' where date like 'May %';")
    cur.execute("update pano set date = substr(date,5,length(date))||'-06' where date like 'Jun %';")
    cur.execute("update pano set date = substr(date,5,length(date))||'-07' where date like 'Jul %';")
    cur.execute("update pano set date = substr(date,5,length(date))||'-08' where date like 'Aug %';")
    cur.execute("update pano set date = substr(date,5,length(date))||'-09' where date like 'Sep %';")
    cur.execute("update pano set date = substr(date,5,length(date))||'-10' where date like 'Oct %';")
    cur.execute("update pano set date = substr(date,5,length(date))||'-11' where date like 'Nov %';")
    cur.execute("update pano set date = substr(date,5,length(date))||'-12' where date like 'Dec %';")
    cur.execute("update pano set `date` = replace(`date`,' ','') where date like ' %'")
    con.commit()
    con.close()
    return 
    
def getlatlng44(): 
    url1 = 'https://www.google.com/maps/@0,0,0a,0y,0h,0t/data=!3m11!1e1!3m9!1s'
    url2 = '!2e10!3e11!6shttps:%2F%2Flh5.googleusercontent.com%2Fp%2F'
    url3 = '%3Dw203-h100-k-no-pi2.6336086-ya5.846676-ro1.5802011-fo100!7i7776!8i3888!9m2!1b1!2i27'
    con = sqlite3.connect('wander.db')
    con.execute("PRAGMA journal_mode=WAL")
    cur = con.cursor()
    cur.execute("select count(*) from pano where panoid like 'AF%' and length(panoid)>40 and panoid_verified is null;")
    end = cur.fetchone()[0]
    if end > 0:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        driver = webdriver.Chrome(options=chrome_options, executable_path='chromedriver')  # Optional argument, if not specified will search path.
        for i in range(0,end):
            if end-i > 1:
                print('records left: ' + str(end-i))
            pano = cur.execute("select panoid from pano where panoid like 'AF%' and length(panoid)>40 and panoid_verified is null LIMIT 1;")
            pano = cur.fetchone()[0]
            url = url1+pano+url2+pano+url3
            try:
                driver.get(url);
            except Exception as e:
                print(e)
                time.sleep(10)
                driver.get(url);
            theurl = driver.current_url
            j=0
            while '@0,0' in theurl:
                time.sleep(1)
                theurl = driver.current_url
                if '@0,0' not in theurl:
                    break
                j+=1
                if j==5:
                    print('waiting 10s more before timeout')
                if j==15:
                    break
            print(theurl)
            if '@0,0' in theurl:
                cur.execute("update pano SET panoid_verified = 'BAD' WHERE panoid = ?;", [pano])
                con.commit()
            else:
                latlng = re.findall(r'@(.*)\,',theurl)
                lat = latlng[0].split(',')[0]
                lng = latlng[0].split(',')[1]
                time.sleep(3)
                #tree = driver.find_elements_by_xpath('//*[@class="widget-titlecard-contentcontainer"]/*')
                tree = driver.find_elements_by_xpath('//*[@id="titlecard"]/*')
                # while len(tree[0].text)<1:
                    # tree = driver.find_elements_by_xpath('//*[@class="titlecard"]/*')
                for i in tree:
                    print(i.text)
                    if 'Street View - ' in i.text:
                        date = i.text.split(' - ')[-1].strip()
                try:
                    
                    if 'Street View - ' in tree[0].text.split('\n')[1].strip():
                        cpr = tree[0].text.split('\n')[0].strip()
                        description = ''
                    else:
                        cpr = tree[0].text.split('\n')[1].strip()
                        description = tree[0].text.split('\n')[0].strip()
                except Exception as e:
                    for i in tree:
                        if len(i.text)>1:
                            cpr = i.text.strip()
                            description = ''
                            break

                geo = rg.search((lat,lng))
                name = geo[0]['name']
                admin1 = geo[0]['admin1']
                admin2 = geo[0]['admin2']
                cc = geo[0]['cc']
                print(lat,'|',lng,'|',description,'|',cpr,'|',date)
                if len(cc)!=2:
                    cur.execute("UPDATE pano SET panoid_verified = ?, lat = ?, lng = ?, copyright = ?, date = ?, description = ? WHERE panoid = ?;",['OK',lat,lng,cpr,date,description,pano])
                else:
                    cur.execute("UPDATE pano SET panoid_verified = ?, lat = ?, lng = ?, copyright = ?, date = ?, description = ?, name = ?, admin1 = ?, admin2 = ?, cc = ? WHERE panoid = ?;",['OK',lat,lng,cpr,date,description,name,admin1,admin2,cc,pano])
                con.commit()
        driver.quit()
        filldb()
    con.close()
    
def getlatlng22():
	# ADD API KEY
    urlbase = 'https://maps.googleapis.com/maps/api/streetview/metadata?key= ADD KEY HERE &pano='
    con = sqlite3.connect('wander.db')
    cur = con.cursor()
    cur.execute("select count(*) from pano where (length(panoid)=22 or length(panoid)=64) and panoid_verified is null and lat is null")
    end = cur.fetchone()[0]
    for i in range(0,end):
        if end-i > 1:
            print('records left: ' + str(end-i))
        pano = cur.execute("select panoid from pano where (length(panoid)=22 or length(panoid)=64) and panoid_verified is null and lat is null LIMIT 1;")
        pano = cur.fetchone()[0]
        try:
            response = requests.get(urlbase+pano)
        except Exception as e:
            print(e)
            time.sleep(10)
            response = requests.get(urlbase+pano)
        if response.json().get('status') == 'OK':
            loc = response.json().get('location')
            lat = loc['lat']
            lng = loc['lng']
            cpr = response.json().get('copyright')[2:]
            date = response.json().get('date')
            geo = rg.search((lat,lng))
            name = geo[0]['name']
            admin1 = geo[0]['admin1']
            admin2 = geo[0]['admin2']
            cc = geo[0]['cc']
            if len(cc)!=2:
                cur.execute("UPDATE pano SET panoid_verified = ?, lat = ?, lng = ?, copyright = ?, date = ? WHERE panoid = ?;",['OK',lat,lng,cpr,date,pano])
            else:
                cur.execute("UPDATE pano SET panoid_verified = ?, lat = ?, lng = ?, copyright = ?, date = ?, name = ?, admin1 = ?, admin2 = ?, cc = ? WHERE panoid = ?;",['OK',lat,lng,cpr,date,name,admin1,admin2,cc,pano])
            # cur.execute("INSERT OR IGNORE INTO pano (panoid) VALUES (?);",[i])
            con.commit()
        else:
            print(pano)
            cur.execute("update pano SET panoid_verified = ? WHERE panoid = ?;",[response.json().get('status'),pano])
            con.commit()
    con.close()
    filldb()
    return

def main(startnum,filename):
    r = open('output.txt','r')
    f = open(filename+'_good.txt','w')
    f2 = open(filename+'_bad.txt','w')
    thumburl22 = 'https://maps.google.com/cbk?output=thumbnail&w=1&h=1&panoid='
    thumburl44a = 'https://lh5.googleusercontent.com/p/'
    thumburl44b = '=w1-h1-p-k-no-pi-10-ya354-ro0-fo100'
	# ADD KEY HERE
    converturl = "https://maps.googleapis.com/maps/api/streetview/metadata?key= ADD KEY HERE &pano="
    n=0
    for panoid in r: 
        n+=1
        if n >= startnum:
            panoid = panoid.strip()
            print(str(n) + ' ' + panoid)
            if n % 100 == 0:
                f.close()
                f2.close()
                f = open(filename+'_good.txt','a+')
                f2 = open(filename+'_bad.txt','a+')

            if len(panoid)<22:
                print('DEL len short')
                # f2.write(panoid+'\n')
            elif panoid[0]=='-' and len(panoid)>45:
                panoid2 = panoid.replace("%2F", "/")
                panoid2='F:'+panoid2
                response = requests.get(converturl+panoid2)
                panoid2 = response.json().get('pano_id')
                if panoid2:
                    print('KEEP successful conversion to ' + panoid2)
                    f.write(panoid2+'\n')
                    # f.write(panoid+'\n')
                else: 
                    print('DEL failed conversion')
                    f2.write(panoid+'\n')

            elif len(panoid) > 40 and len(panoid)<50 and panoid[:2]=='AF':
                response = requests.get(thumburl44a + panoid + thumburl44b,timeout=10)
                if response.status_code!=404:
                    print(thumburl44a+panoid + ' KEEP 200')
                    f.write(panoid+'\n')
                else:
                    print(thumburl44a+panoid + ' DEL 404')
                    f2.write(panoid+'\n')
            elif len(panoid)>22:
                print('KEEP len long')
                f.write(panoid+'\n')
            else:
                response = requests.get(thumburl22+panoid,timeout=10)
                if response.status_code!=404:
                    print(thumburl22+panoid + ' KEEP 200')
                    f.write(panoid+'\n')
                else:
                    print(thumburl22+panoid + ' DEL 404')
                    f2.write(panoid+'\n')
            
    f.close()
    f2.close()


if __name__ == "__main__":

    # if len(sys.argv)==2:
        # filename=sys.argv[1]
        # startnum=0
    # elif len(sys.argv)==3:
        # filename=sys.argv[1]
        # startnum=int(sys.argv[2])
    # else:
        # filename='tmp'
        # startnum=1
    getlatlng22()
    getlatlng44()
    # main(startnum,filename)
        
