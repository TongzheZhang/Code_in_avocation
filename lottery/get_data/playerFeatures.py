# -*- coding: utf-8 -*-
"""
Created on Mon May 28 13:40:26 2018

@author: Administrator
"""
from bs4 import BeautifulSoup
import pandas as pd
import re
from sqlalchemy import create_engine 
import requests
from sqlalchemy.types import NVARCHAR, Float, Integer

file = open('C:/Users/Administrator/Desktop/yingchao_season_score/PlayerIDList.txt','r')  
PlayerIDList = file.read()
file.close()
PlayerIDList = eval(PlayerIDList) #将str还原为list

#driver = webdriver.PhantomJS(executable_path = 'D:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')

symbols = {}
for IDnum, ID in enumerate(PlayerIDList):
#for IDnum in range(13,14):
    url = "https://sofifa.com/player/"+ID
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Language': 'zh-CN',
           'Cache-Control': 'max-age=0',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.2.2.2000',
           }

    pageSource = requests.get(url).text
    html_parse = BeautifulSoup(pageSource)
    table = html_parse.findAll('article',{'class':'column'})[0] 
    s = {}
    info = table.findAll('div',{'class':'meta'})[0]
    infotext = info.select('span')[0].text
    #通过split,得到name, age, birth
    infospt = infotext.split('  ')
    s['name'] = infospt[0]
    '''
    a = infospt[1].split(' ')
    s['age'] = a[3]
    b = infospt[1].split('(')
    c = b[1].split(')')
    s['birth'] = c[0]
    '''
    s['ID'] = PlayerIDList[0]
    general_rating = table.findAll('div',{'class':'stats'})[0]
    tds = general_rating.select('td')[0:]
    
    overall_rating = tds[0].select('span')[0]
    s['overall_rating'] = int(overall_rating.text)
    potential = tds[1].select('span')[0]
    s['potential'] = int(potential.text)
    value = tds[2].select('span')[0]
    s['value'] = value.text
    wage = tds[3].select('span')[0]
    s['wage'] = wage.text
    
    teaminfo = table.findAll('div',{'class':'teams'})[0]
    teamtds = teaminfo.select('td')[2:]
    for i,td in enumerate(teamtds):
        try:
            li = td.select('li')[0:]
            s['group'+str(i)] = li[0].text
            s['group_rating'+str(i)] = li[1].select('span')[0].text
            numList = re.compile('\d').findall(str(li[3]))
            Jersey = "".join(numList)
            s['JerseyNumber'+str(i)] = Jersey
        except IndexError:
            pass
    Attackinginfo = table.findAll('div',{'class':'column col-3 mb-20'})[0]
    AttackLi = Attackinginfo.select('li')[0:]
    s['Crossing'] = int(AttackLi[0].select('span')[0].text)
    s['Finishing'] = int(AttackLi[1].select('span')[0].text)
    s['HeadAccuracy'] = int(AttackLi[2].select('span')[0].text)
    s['ShortPassion'] = int(AttackLi[3].select('span')[0].text)
    s['Volleys'] = int(AttackLi[4].select('span')[0].text)
    
    GoalKeepinginfo = table.findAll('div',{'class':'column col-3 mb-20'})[6]
    GoalKeepingLi = GoalKeepinginfo.select('li')[0:]
    s['GKDiving'] = int(GoalKeepingLi[0].select('span')[0].text)
    s['GKHanding'] = int(GoalKeepingLi[1].select('span')[0].text)
    s['GKKicking'] = int(GoalKeepingLi[2].select('span')[0].text)
    s['GKPositioning'] = int(GoalKeepingLi[3].select('span')[0].text)
    s['GKReflexes'] = int(GoalKeepingLi[4].select('span')[0].text)
    symbols[IDnum] = s

df = pd.DataFrame(symbols).T 
        
dtypedict = {
      'name': NVARCHAR(length=255),
      #'age': NVARCHAR(length=255),
      #'birth': NVARCHAR(length=255),
      'ID': NVARCHAR(length=255),

      'value': NVARCHAR(length=255),
      'wage': NVARCHAR(length=255),

      'overall_rating': Integer(),
      'potential': Integer(),
      'Crossing': Integer(),
      'Finishing': Integer(),
      'HeadAccuracy': Integer(),
      'ShortPassion': Integer(),
      'Volleys': Integer(),
      'GKDiving': Integer(),
      'GKHanding': Integer(),
      'GKKicking': Integer(),
      'GKPositioning': Integer(),
      'GKReflexes': Integer()

    }
    
yconnect = create_engine('mysql+mysqldb://root:@127.0.0.1:3306/zucai?charset=utf8') 
pd.io.sql.to_sql(df,'PlayerFeatures', yconnect, schema='zucai', if_exists='append',dtype=dtypedict)  