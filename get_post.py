import numpy as np
import pandas as pd

import requests
from bs4 import BeautifulSoup

import MySQLdb as mdb
import sys
import traceback

#获取城市名称和相应的超链接
r = requests.get('http://ip138.com/post/')
text = r.text.encode('iso-8859-1').decode('gb2312')
bs = BeautifulSoup(text,'html5lib')
links = bs.select('div#newAlexa > table.t4 > tbody > tr > td > a')
links_list=[]
for link in links:
    links_list.append((link.text,'http://ip138.com'+link.get('href')))

data={}
#获取各个城市的邮编
for city in links_list:
    city_ip=[]
    r2 = requests.get(city[1])
    text2 = r2.text.encode('iso-8859-1').decode('gb18030')
    bs2 = BeautifulSoup(text2,'html5lib')
    ip_table = bs2.select('table.t12 > tbody > tr')
    for i in range(1,len(ip_table)):
        little_city = ip_table[i]
        tds = little_city.select('td')
        for j in range(len(tds)//3):
            name = tds[j*3].text
            post = tds[j*3+1].text
            phone = tds[j*3+2].text
            city_ip.append([name,post,phone])
    data[city[0]]=city_ip

para=[]
for key in data.keys():
    for little_city in data[key]:
        para.append([i]+little_city)
        i += 1

datac=pd.DataFrame(index=range(len(para)))
datac=pd.DataFrame(para,index=range(len(para)))

with open('cityip.csv','w+') as f:
    datac.to_csv(f)

f.close()


#存入mysql中
con=mdb.connect(host='localhost',
                user='root',db='lqj',passwd='123456',
                use_unicode=True,charset='utf8')
cur=con.cursor()
sql="""insert into cityip(id,name,post,phone) values(%s,%s,%s,%s)"""
i=0

try:
    cur.executemany(sql,para)
except:
    traceback.print_exc()
    
con.commit()
        




        
        
                         
    



