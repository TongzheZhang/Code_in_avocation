# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 10:47:44 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 14:37:25 2018

@author: Administrator
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import MySQLdb
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Float, Integer

driver = webdriver.PhantomJS(executable_path = 'D:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')    
'''
year = 2018
urllist_set = [['http://www.okooo.com/soccer/league/308/schedule/12033/2-7238/',
           'http://www.okooo.com/soccer/league/308/schedule/12033/2-7239/',
           'http://www.okooo.com/soccer/league/308/schedule/12033/2-7240/',
           'http://www.okooo.com/soccer/league/308/schedule/12033/2-7241/',
           'http://www.okooo.com/soccer/league/308/schedule/12033/2-7256/',
           'http://www.okooo.com/soccer/league/308/schedule/12033/2-38807/',
           'http://www.okooo.com/soccer/league/308/schedule/12033/2-38805/',
           'http://www.okooo.com/soccer/league/308/schedule/12033/2-38806/'],
           ['http://www.okooo.com/soccer/league/11/schedule/12253/1-1757/',
           'http://www.okooo.com/soccer/league/11/schedule/12253/1-1758/',
           'http://www.okooo.com/soccer/league/11/schedule/12253/1-1759/',
           'http://www.okooo.com/soccer/league/11/schedule/12253/1-1760/',
           'http://www.okooo.com/soccer/league/11/schedule/12253/1-1761/',
           'http://www.okooo.com/soccer/league/11/schedule/12253/1-1762/',
           'http://www.okooo.com/soccer/league/11/schedule/12253/1-1763/',
           'http://www.okooo.com/soccer/league/11/schedule/12253/1-1764/',
           'http://www.okooo.com/soccer/league/11/schedule/12253/1-7255/'],
           ['http://www.okooo.com/soccer/league/13/schedule/12251/2-9360/',
            'http://www.okooo.com/soccer/league/13/schedule/12251/2-9361/',
            'http://www.okooo.com/soccer/league/13/schedule/12251/2-9362/',
            'http://www.okooo.com/soccer/league/13/schedule/12251/2-9363/',
            'http://www.okooo.com/soccer/league/13/schedule/12251/2-9364/'],
           ['http://www.okooo.com/soccer/league/14/schedule/12022/2-38899/',
            'http://www.okooo.com/soccer/league/14/schedule/12022/2-38900/',
            'http://www.okooo.com/soccer/league/14/schedule/12022/2-38898/']
           ]           
'''
'''
year = 2014
urllist_set = [['http://www.okooo.com/soccer/league/308/schedule/3319/2-7238/',
           'http://www.okooo.com/soccer/league/308/schedule/3319/2-7239/',
           'http://www.okooo.com/soccer/league/308/schedule/3319/2-7240/',
           'http://www.okooo.com/soccer/league/308/schedule/3319/2-7241/',
           'http://www.okooo.com/soccer/league/308/schedule/3319/2-7256/'],
           ['http://www.okooo.com/soccer/league/11/schedule/3657/1-1757/',
           'http://www.okooo.com/soccer/league/11/schedule/3657/1-1758/',
           'http://www.okooo.com/soccer/league/11/schedule/3657/1-1759/',
           'http://www.okooo.com/soccer/league/11/schedule/3657/1-1760/',
           'http://www.okooo.com/soccer/league/11/schedule/3657/1-1761/',
           'http://www.okooo.com/soccer/league/11/schedule/3657/1-1762/',
           'http://www.okooo.com/soccer/league/11/schedule/3657/1-1763/',
           'http://www.okooo.com/soccer/league/11/schedule/3657/1-1764/',
           'http://www.okooo.com/soccer/league/11/schedule/3657/1-7255/'],
           ['http://www.okooo.com/soccer/league/13/schedule/3877/2-9360/',
            'http://www.okooo.com/soccer/league/13/schedule/3877/2-9361/',
            'http://www.okooo.com/soccer/league/13/schedule/3877/2-9362/',
            'http://www.okooo.com/soccer/league/13/schedule/3877/2-9363/',
            'http://www.okooo.com/soccer/league/13/schedule/3877/2-9364/',
            'http://www.okooo.com/soccer/league/13/schedule/3877/2-7247/',
            'http://www.okooo.com/soccer/league/13/schedule/3877/2-7249/',
            'http://www.okooo.com/soccer/league/13/schedule/3877/2-7250/',
            'http://www.okooo.com/soccer/league/13/schedule/3877/2-7251/',
            'http://www.okooo.com/soccer/league/13/schedule/3877/2-7252/'],
            ['http://www.okooo.com/soccer/league/14/schedule/3358/3-8514/',
            'http://www.okooo.com/soccer/league/14/schedule/3358/3-8515/',
            'http://www.okooo.com/soccer/league/14/schedule/3358/3-8516/']
           ]  
'''

year = 2010
urllist_set = [['http://www.okooo.com/soccer/league/308/schedule/1000/2-7238/',
           'http://www.okooo.com/soccer/league/308/schedule/1000/2-7239/',
           'http://www.okooo.com/soccer/league/308/schedule/1000/2-7240/',
           'http://www.okooo.com/soccer/league/308/schedule/1000/2-7241/',
           'http://www.okooo.com/soccer/league/308/schedule/1000/2-7256/'],
           ['http://www.okooo.com/soccer/league/11/schedule/1152/1-1757/',
           'http://www.okooo.com/soccer/league/11/schedule/1152/1-1758/',
           'http://www.okooo.com/soccer/league/11/schedule/1152/1-1759/',
           'http://www.okooo.com/soccer/league/11/schedule/1152/1-1760/',
           'http://www.okooo.com/soccer/league/11/schedule/1152/1-1761/',
           'http://www.okooo.com/soccer/league/11/schedule/1152/1-1762/',
           'http://www.okooo.com/soccer/league/11/schedule/1152/1-1763/',
           'http://www.okooo.com/soccer/league/11/schedule/1152/1-1764/',
           'http://www.okooo.com/soccer/league/11/schedule/1152/1-7255/'],
           ['http://www.okooo.com/soccer/league/13/schedule/1002/2-9360/',
            'http://www.okooo.com/soccer/league/13/schedule/1002/2-9361/',
            'http://www.okooo.com/soccer/league/13/schedule/1002/2-9362/',
            'http://www.okooo.com/soccer/league/13/schedule/1002/2-9363/',
            'http://www.okooo.com/soccer/league/13/schedule/1002/2-9364/',
            'http://www.okooo.com/soccer/league/13/schedule/1002/2-7247/',
            'http://www.okooo.com/soccer/league/13/schedule/1002/2-7249/',
            'http://www.okooo.com/soccer/league/13/schedule/1002/2-7250/',
            'http://www.okooo.com/soccer/league/13/schedule/1002/2-7251/',
            'http://www.okooo.com/soccer/league/13/schedule/1002/2-7252/'],
            ['http://www.okooo.com/soccer/league/14/schedule/1154/2-8514/',
            'http://www.okooo.com/soccer/league/14/schedule/1154/2-8515/',
            'http://www.okooo.com/soccer/league/14/schedule/1154/2-8516/']
           ]  

        
           
name = ['Precentral_Asia','Precentral_Europe','Precentral_Africa','Precentral_North_America']    

for j,urllist in enumerate(urllist_set):
    for url in urllist:
        driver.get(url)
        pageSource = driver.page_source
        html_parse = BeautifulSoup(pageSource)
        table = html_parse.findAll('div',{'id':'main1'})[0] 
        #print table
        symbolslist = table.select('tr')[2:]
        symbols = {}    
        for i, symbol in enumerate(symbolslist):
            tds = symbol.select('td')
            s = {}
            
            s['rank'] = tds[0].text  # 排名
            s['Team'] = tds[1].text  # 球队    
            s['game_num'] = tds[2].text  # 比赛场数
            s['win'] = tds[3].text  # 获胜场数            
            s['draw'] = tds[4].text  # 平
            s['lose'] = tds[5].text  # 输球场数
            s['goals_scored'] = tds[6].text  # 进球个数
            s['goals_against'] = tds[7].text  # 失球个数
            s['goals_net'] = tds[8].text  # 进球-失球
        
            s['host_game_num'] = tds[9].text  # 比赛场数
            s['host_win'] = tds[10].text  # 获胜场数            
            s['host_draw'] = tds[11].text  # 平
            s['host_lose'] = tds[12].text  # 输球场数
            s['host_goals_scored'] = tds[13].text  # 进球个数
            s['host_goals_against'] = tds[14].text  # 失球个数
            
            s['guest_game_num'] = tds[15].text  # 比赛场数
            s['guest_win'] = tds[16].text  # 获胜场数            
            s['guest_draw'] = tds[17].text  # 平
            s['guest_lose'] = tds[18].text  # 输球场数
            s['guest_goals_scored'] = tds[19].text  # 进球个数
            s['guest_goals_against'] = tds[20].text  # 失球个数
            
            symbols[i] = s
        #print symbols
        df_symbols = pd.DataFrame(symbols).T
    
        dtypedict = {
          'rank': Integer(),
          'Team': NVARCHAR(length=255),
          'game_num': Integer(),
          'win': Integer(),
          'draw': Integer(),
          'lose': Integer(),
          'goals_scored': Integer(),
          'goal_against': Integer(),
          'goals_net': Integer(),
    
          'host_game_num': Integer(),
          'host_win': Integer(),
          'host_draw': Integer(),
          'host_lose': Integer(),
          'host_goals_scored': Integer(),
          'host_goals_against': Integer(),
    
          'guest_game_num': Integer(),
          'guest_win': Integer(),
          'guest_draw': Integer(),
          'guest_lose': Integer(),
          'guest_goals_scored': Integer(),
          'guest_goals_against': Integer(),
        }
        
        yconnect = create_engine('mysql+mysqldb://root:@127.0.0.1:3306/zucai?charset=utf8') 
        pd.io.sql.to_sql(df_symbols, name[j]+str(year), yconnect, schema='zucai', if_exists='append',dtype=dtypedict)  
    
