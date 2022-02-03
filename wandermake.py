import pandas as pd
import sys, json, random, re, sqlite3
from builtins import str
import unidecode
import codecs
import wanderclean, wanderscrape, wanderorganize

def makedirs(m,df):
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
    
    
def makedir(title,isFolder,folderContents,timeStamp):
    dfdir = pd.DataFrame({'title': title,
                       'isfolder': isFolder,
                       'folderContents': folderContents,
                       'timeStamp': timeStamp
                       })
    return dfdir
    
def makepano(panoid,title,timeStamp):
    dfpano = pd.DataFrame({'panoid': [panoid],
                       'title': [title],
                       'isfolder': ['false'],
                       'timeStamp': [1]
                   })
                   

                   

if __name__ == "__main__":
   
    con = sqlite3.connect('wander.db')
    cur = con.cursor()
    cur.execute("select Country_Name from pano a left join svf_pages b on a.panoid=b.panoid join continent c on a.cc=c.Two_Letter_Country_Code where panoid_verified='OK' and svf_url is null and copyright is not null and copyright != 'Underwater Earth'  group by cc  having count(*)>50 order by count(*) desc;")
    folders = cur.fetchall()
    title, isFolder, folderContents, timeStamp = [], [], [], []
    for folder in folders:
        title.append(folder[0])
        isFolder.append('true')
        folderContents.append('[]')
        timeStamp.append(1)
        cur.execute("select panoid, title from pano a left join svf_pages b on a.panoid=b.panoid join continent c on a.cc=c.Two_Letter_Country_Code where panoid_verified='OK' and svf_url is null and copyright is not null and copyright != 'Underwater Earth' where Country_Name = ?", folder[0])
        panos = cur.fetchall()
        panoid, title, isFolder, timeStamp = []
        for pano in panos:
            panoid.append(panos[0])
            title.append(panos[1])
            isFolder.append('false')
            timeStamp.append(2)
            
            # df.at[i,'folderContents'] =
    print(makedir(title, isFolder, folderContents, timeStamp))
    
    for i in 
        
    # print(folders[0])
    # makedir(
    # dictDir = {}
    # for folder in folders:
        # dictDir[folder[0]]=makedir(folder[0])
    con.close()
    # print(dictDir)
    
    
    
    
