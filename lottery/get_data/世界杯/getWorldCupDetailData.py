# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 13:19:25 2018

@author: Administrator
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
from sqlalchemy import create_engine 
from sqlalchemy.types import NVARCHAR, Float, Integer

driver = webdriver.PhantomJS(executable_path = 'D:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
'''
year = 2014
urllist = ["http://www.okooo.com/soccer/league/16/schedule/11689/1-3954/?show=all",
           "http://www.okooo.com/soccer/league/16/schedule/11689/1-3955/?show=all",
           "http://www.okooo.com/soccer/league/16/schedule/11689/1-3956/?show=all",
           "http://www.okooo.com/soccer/league/16/schedule/11689/1-3957/?show=all",
           "http://www.okooo.com/soccer/league/16/schedule/11689/1-3958/?show=all",
           "http://www.okooo.com/soccer/league/16/schedule/11689/1-3959/?show=all",
           "http://www.okooo.com/soccer/league/16/schedule/11689/1-3960/?show=all",
           "http://www.okooo.com/soccer/league/16/schedule/11689/1-3961/?show=all"]
'''
year = 2010
urllist = ["http://www.okooo.com/soccer/league/16/schedule/2531/1-3954/?show=all   ",
           "http://www.okooo.com/soccer/league/16/schedule/2531/1-3955/?show=all",
           "http://www.okooo.com/soccer/league/16/schedule/2531/1-3956/?show=all",
           "http://www.okooo.com/soccer/league/16/schedule/2531/1-3957/?show=all",
           "http://www.okooo.com/soccer/league/16/schedule/2531/1-3958/?show=all",
           "http://www.okooo.com/soccer/league/16/schedule/2531/1-3959/?show=all",
           "http://www.okooo.com/soccer/league/16/schedule/2531/1-3960/?show=all",
           "http://www.okooo.com/soccer/league/16/schedule/2531/1-3961/?show=all"]
        
#爬取数据（比赛场次，比分，赔率等）
symbols = {}
j = 0
for index,url in enumerate(urllist):
    driver.get(url)
    pageSource = driver.page_source
    
    html_parse = BeautifulSoup(pageSource)
    table = html_parse.findAll('table',{'id':'team_fight_table'})[0] 
    #print table
    symbolslist = table.select('tr')[1:]
    for symbol in symbolslist:
        tds = symbol.select('td')
        s = {}
        s['time'] = tds[0].text  # Time
        s['round'] = tds[1].text  # 第几轮    
        s['host'] = tds[2].text  # Host
        s['score'] = tds[3].text  # 第几轮            
        s['guest'] = tds[4].text  # Guest
        s['chupei_win'] = tds[5].text  # 赔率
        s['chupei_draw'] = tds[6].text  # 赔率
        s['chupei_lose'] = tds[7].text  # 赔率     
        symbols[j] = s      
        j = j + 1  
    
df_symbols = pd.DataFrame(symbols).T 
#数据清洗，将已完成的比赛筛选出来
df_symbols['finished_or_not'] = map(lambda x:re.search('\d',df_symbols['score'].ix[x],flags=0) == None,[y for y in range(len(df_symbols))])
finished_matches = df_symbols.loc[df_symbols['finished_or_not']==False]
finished_matches = finished_matches.reset_index(drop=True) #index重新定义
#a = df_odds_scores[df_odds_scores['时间']=='04-08 23:30'].index.tolist() 
#scores = df_odds_scores['比分'] 
#finished_matches = df_odds_scores.ix[0:a[0]] #只取比赛完成的部分
scores = finished_matches['score'] 
new_scores = scores.str.split('-',expand = True) #去除比分中的“-”
new_scores = new_scores.astype('int') #将比分变为整数

finished_matches['host_score'] = new_scores.ix[:,0]  
finished_matches['guest_score'] = new_scores.ix[:,1]                      
finished_matches['Team'] =  finished_matches['host'] + finished_matches['guest'] 
finished_matches['Team'] =  finished_matches['Team'].str.replace(' ','')                  
finished_matches.to_csv('C:/Users/Administrator/Desktop/worldcup_detail%s.csv'%year,encoding='gbk') 
#finished_matches['赛果'] = 0
#finished_matches = finished_matches.reindex(range(len(finished_matches.index)))
finished_matches['result'] = 0
for i in range(len(finished_matches)):                
    if finished_matches['host_score'].ix[i] > finished_matches['guest_score'].ix[i]:
        finished_matches['result'].ix[i] = 'win'
    elif finished_matches['host_score'].ix[i] < finished_matches['guest_score'].ix[i]:
        finished_matches['result'].ix[i] = 'lose'
    else: 
        finished_matches['result'].ix[i] = 'draw'    

dtypedict = {
  'guest': NVARCHAR(length=255),
  'host': NVARCHAR(length=255),
  'score': NVARCHAR(length=255),
  'Team': NVARCHAR(length=255),
  'round': Integer(),
  'host_score': Integer(),
  'guest_score': Integer(),
  'chupei_win': Float(),
  'chupei_draw': Float(),
  'chupei_lose': Float()
}

yconnect = create_engine('mysql+mysqldb://root:@127.0.0.1:3306/zucai?charset=utf8') 
pd.io.sql.to_sql(finished_matches,'worldcup_dataildata'+str(year), yconnect, schema='zucai', if_exists='replace',dtype=dtypedict)  