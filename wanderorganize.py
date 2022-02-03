import pandas as pd
import sys, json, random, re
import sqlite3
from builtins import str
import unidecode
import codecs
import wanderclean, wanderscrape

def unidecode_fallback(e):
    part = e.object[e.start:e.end]
    replacement = str(unidecode.unidecode(part) or '?')
    return (replacement, e.start + len(part))

def denull():
    with open('Wander_Favorites.json', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace(',"panoid":null', '')
    filedata = filedata.replace(',"folderContents":null', '')
    filedata = filedata.replace(',"description":null', '')
    filedata = filedata.replace('{"panoid":null,','{')
    filedata = filedata.replace('"title":null,','"title":"NA"')
    filedata = str(filedata)
    with open('Wander_Favorites.json', 'w') as file:
        file.write(filedata)
    return

def newstuff():
    with open('Wander_Favorites.json', 'r') as file:
        filedata = file.read()
    filedata = filedata[:-1]
    con = sqlite3.connect('wander.db')
    cur = con.cursor()
    cur.execute('select \'{"panoid":"\'||panoid||\'","title":"\'||cc||\'|\'||admin1||\'|\'||name||\'","isFolder":false,"timeStamp":\'||cast(julianday(timestamp)*10000000 as int)||\'},\' as newtitle from pano where timestamp > date("now", "-70 day") and panoid_verified = "OK" order by timestamp desc limit 4000;')
    # cur.execute('select \'{"panoid":"\'||panoid||\'","title":"\'||cc||\'|\'||admin1||\'|\'||name||\'","isFolder":false,"timeStamp":\'||637628674067364870\'},\' as newtitle from pano where timestamp > date("now", "-70 day") and panoid_verified = "OK" order by timestamp desc limit 4000;')
    newq = cur.fetchall()   
    con.close()
    filedata += ',{"title":"!new stuff","isFolder":true,"folderContents":['
    n=0
    for i in newq:
        n+=1
        if n == len(newq):
            filedata += i[0][:-1]
        else:
            # j = i[0].split('"title":"')
            # filedata += j[0] + '"title":"' + str(n) + '|' + j[1]
            filedata += i[0]
    filedata += '],"timeStamp":537833618319444000}]'   
    codecs.register_error('unidecode_fallback', unidecode_fallback)
    s = filedata.encode('iso-8859-1', errors='unidecode_fallback')
    filedata = s.decode('iso-8859-1')
    with open('Wander_Favorites.json', 'w') as file:
        file.write(filedata)
    return
    
def newstuffalpha():
    with open('Wander_Favorites.json', 'r') as file:
        filedata = file.read()
    filedata = filedata[:-1]
    con = sqlite3.connect('wander.db')
    cur = con.cursor()
    cur.execute('select \'{"panoid":"\'||panoid||\'","title":"\'||cc||\'|\'||admin1||\'|\'||name||\'","isFolder":false,"timeStamp":\'||cast(julianday(timestamp)*10000000 as int)||\'},\' as newtitle from pano where timestamp > date("now", "-25 day") and panoid_verified = "OK" order by timestamp desc limit 4000;')
    #cur.execute('select \'{"panoid":"\'||panoid||\'","title":"\'||title||\'","isFolder":false,"timeStamp":\'||cast(julianday(timestamp)*10000000 as int)||\'},\' as newtitle from pano where timestamp > date("now", "-25 day") and panoid_verified = "OK" order by timestamp desc limit 4000;')
    newq = cur.fetchall()   
    con.close()
    filedata += ',{"title":"!new stuff alpha","isFolder":true,"folderContents":['
    n=0
    for i in newq:
        n+=1
        if n == len(newq):
            filedata += i[0][:-1]
        else:
            filedata += i[0]
    filedata += '],"timeStamp":537833618319444000}]'   
    codecs.register_error('unidecode_fallback', unidecode_fallback)
    s = filedata.encode('iso-8859-1', errors='unidecode_fallback')
    filedata = s.decode('iso-8859-1')
    with open('Wander_Favorites.json', 'w') as file:
        file.write(filedata)
    return
    
def organize(m,df):
    m+=1
    df = df.sort_values(by=['isFolder', 'title'],ascending=False,ignore_index=True)
    #set timestamp to index (alphabetically order entries in current df)
    df["timeStamp"]=df.index + ( m * 100000 ) + 137592382515497210 
    for i in range(0,len(df.index)):
        if df.at[i,'isFolder'] == True: 
            if len(df.at[i,'folderContents'])>0:
                # print(df.at[i,'title'])
                df1 = pd.DataFrame(eval(str(df.at[i,'folderContents'])))
                df1 = df1.sort_values(by=['isFolder', 'title'],ascending=False,ignore_index=True)
                df1["timeStamp"]=df1.index + ( m * 100000 ) + 237592382515497210
                #pass new dataframe for recursion
                df.at[i,'folderContents']=organize(m,df1)
    return df

    
def rename(df):
    con = sqlite3.connect('wander.db')
    cur = con.cursor()
    for i in range(0,len(df.index)):
        #folder renaming
        if df.at[i,'isFolder'] == True:
            #ignore certain folders
            if '!new stuff' not in df.at[i,'title']: 
                if len(df.at[i,'folderContents'])>0:        
                    df1 = pd.DataFrame(eval(str(df.at[i,'folderContents'])))
                    if '|' in df.at[i,'title']:
                        df.at[i,'title'] = df.at[i,'title'].split('|')[0] + '|' + str(len(df1.index))
                    else:
                        df.at[i,'title'] = df.at[i,'title'] + '|' + str(len(df1.index))
                    print(df.at[i,'title'])
                    df.at[i,'folderContents'] = rename(df1)
                #empty folder
                else:
                    if '|' in df.at[i,'title']:
                        df.at[i,'title'] = df.at[i,'title'].split('|')[0] + '|0' 
                    else:
                        df.at[i,'title'] = df.at[i,'title'] + '|0'
                    print(df.at[i,'title'])
        #pano renaming
        else:
            pano = df.at[i,'panoid']
            wander_title = df.at[i,'title']
            if wander_title[2:3] != '|':
                cur.execute("select title, panoid_verified from pano where panoid = ? ;",[pano])
                newtitle = cur.fetchone()
                if newtitle == None and df.at[i,'isFolder'] != 1:
                    wander_title = df.at[i,'title']
                    print('not in db... adding ',(pano, wander_title))
                    cur.execute("INSERT OR IGNORE INTO pano (panoid, wander_title) VALUES (?, ?);",[pano, wander_title])
                    con.commit()
                    wanderclean.getlatlng22()
                    wanderclean.getlatlng44()
                    cur.execute("select title, panoid_verified from pano where panoid = ? ;",[pano])
                    newtitle = cur.fetchone()
                if newtitle != None:
                    badtitle = newtitle[1]
                    newtitle = newtitle[0]
                    if newtitle == None:
                        if badtitle != None:
                            newtitle = '!!!' + badtitle
                        else:
                            newtitle = '!!!unknown'
                    # print(newtitle)
                    wander_title = df.at[i,'title']
                    cur.execute("update pano set wander_title = ? where panoid = ? and wander_title is null ;",[wander_title, pano])
                    con.commit()
                    codecs.register_error('unidecode_fallback', unidecode_fallback)
                    s = newtitle.encode('iso-8859-1', errors='unidecode_fallback')
                    newtitle = s.decode('iso-8859-1')
                    if len(newtitle)>40:
                        newtitle = newtitle.replace(' ','')
                        newtitle = newtitle.replace('-','')
                    # print(newtitle[:45])
                    df.at[i,'title'] = newtitle[:45]
    #exclude folder '!new stuff' before writing
    df = df[df.title != '!new stuff']
    df = df[df.title != '!new stuff alpha']
    con.close()
    return df
    
def isUsed(df,folderName='default'):
    chunk = []
    for i in range(0,len(df.index)):
        #folder renaming
        if df.at[i,'isFolder'] == True:
            #ignore certain folders
            if '!new stuff' not in df.at[i,'title']: 
                if len(df.at[i,'folderContents'])>0:        
                    df1 = pd.DataFrame(eval(str(df.at[i,'folderContents'])))
                    if '|' in df.at[i,'title']:
                        folderName = df.at[i,'title'].split('|')[0]
                    else:
                        folderName = df.at[i,'title']
                    # print(folderName)
                    df.at[i,'folderContents'] = isUsed(df1,folderName)
        #add panos
        else:
            pano = df.at[i,'panoid']
            chunk.append((df.at[i,'panoid'],folderName))
    con = sqlite3.connect('wander.db')
    cur = con.cursor()
    cur.executemany("INSERT OR IGNORE INTO folders (panoid, folder) VALUES (?, ?);",chunk)
    con.commit()
    con.close()
    return df

if __name__ == "__main__":
    file = 'c:\\users\\inaun\\wander_favorites.json'
    
    print('=== scraping svf ===')
    wanderscrape.svf()
    
    print('=== renaming ===')
    df = pd.read_json(file)
    renamed_df = rename(df)
    renamed_df.to_json(file,orient='records')
    
    print('=== adding newstuff alpha folder ===')
    newstuffalpha()
    
    print('=== organizing ===')
    df = pd.read_json(file)
    organized_df = organize(0,df)
    organized_df.to_json(file,orient='records')
    
    print('=== adding newstuff folder ===')
    newstuff()
    
    # print('=== updating folders db ===')
    # df = pd.read_json(file)
    # isUsed(df)
    
    # denull()

