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
urllist_set = [["http://www.okooo.com/soccer/league/17/schedule/13222/",
    "http://www.okooo.com/soccer/league/17/schedule/12651/",
    "http://www.okooo.com/soccer/league/17/schedule/12084/",
    "http://www.okooo.com/soccer/league/17/schedule/8186/"],
    ["http://www.okooo.com/soccer/league/23/schedule/13347/",
    "http://www.okooo.com/soccer/league/23/schedule/12786/",
    "http://www.okooo.com/soccer/league/23/schedule/12257/",
    "http://www.okooo.com/soccer/league/23/schedule/8618/"],
    ["http://www.okooo.com/soccer/league/8/schedule/13342/",
    "http://www.okooo.com/soccer/league/8/schedule/12749/",
    "http://www.okooo.com/soccer/league/8/schedule/12176/",
    "http://www.okooo.com/soccer/league/8/schedule/8578/"],
    ["http://www.okooo.com/soccer/league/35/schedule/13262/",
    "http://www.okooo.com/soccer/league/35/schedule/12694/1/",
    "http://www.okooo.com/soccer/league/35/schedule/12137/1/",
    "http://www.okooo.com/soccer/league/35/schedule/8238/1/"],
    ["http://www.okooo.com/soccer/league/34/schedule/13224/",
    "http://www.okooo.com/soccer/league/34/schedule/12639/1/",
     "http://www.okooo.com/soccer/league/34/schedule/12095/",
     "http://www.okooo.com/soccer/league/34/schedule/8122/"],
    ["http://www.okooo.com/soccer/league/196/schedule/13046/",
     "http://www.okooo.com/soccer/league/196/schedule/12540/1/",
     "http://www.okooo.com/soccer/league/196/schedule/11930/1/"],
    ["http://www.okooo.com/soccer/league/410/schedule/13055/1/",
     "http://www.okooo.com/soccer/league/410/schedule/12537/1/",
     "http://www.okooo.com/soccer/league/410/schedule/11956/1/"],
    ["http://www.okooo.com/soccer/league/182/schedule/12641/1/",
     "http://www.okooo.com/soccer/league/182/schedule/12096/",
     "http://www.okooo.com/soccer/league/182/schedule/8124/"],
    ["http://www.okooo.com/soccer/league/44/schedule/12695/1/",
     "http://www.okooo.com/soccer/league/44/schedule/12136/1/",
     "http://www.okooo.com/soccer/league/44/schedule/8240/1/"]]
'''
urllist_set = [["http://www.okooo.com/soccer/league/17/schedule/13222/",
    "http://www.okooo.com/soccer/league/17/schedule/12651/",
    "http://www.okooo.com/soccer/league/17/schedule/12084/",
    "http://www.okooo.com/soccer/league/17/schedule/8186/"],
    ["http://www.okooo.com/soccer/league/23/schedule/13347/",
    "http://www.okooo.com/soccer/league/23/schedule/12786/",
    "http://www.okooo.com/soccer/league/23/schedule/12257/",
    "http://www.okooo.com/soccer/league/23/schedule/8618/"],
    ["http://www.okooo.com/soccer/league/8/schedule/13342/",
    "http://www.okooo.com/soccer/league/8/schedule/12749/",
    "http://www.okooo.com/soccer/league/8/schedule/12176/",
    "http://www.okooo.com/soccer/league/8/schedule/8578/"],
    ["http://www.okooo.com/soccer/league/35/schedule/13262/",
    "http://www.okooo.com/soccer/league/35/schedule/12694/1/",
    "http://www.okooo.com/soccer/league/35/schedule/12137/1/",
    "http://www.okooo.com/soccer/league/35/schedule/8238/1/"],
    ["http://www.okooo.com/soccer/league/34/schedule/13224/",
    "http://www.okooo.com/soccer/league/34/schedule/12639/1/",
     "http://www.okooo.com/soccer/league/34/schedule/12095/",
     "http://www.okooo.com/soccer/league/34/schedule/8122/"]]
'''     
name = ['English_Premier_League','Italy_Serie_A','Spanish_La_Liga',
'German_Bundesliga','France_Ligue_one','J_League','K_League','France_Ligue_two','German_B']    
'''
name = ['English_Premier_League','Italy_Serie_A','Spanish_La_Liga',
'German_Bundesliga','France_Ligue_one']    

for j in range(len(urllist_set)):
    year = 18
    urllist = urllist_set[j]
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
            
            #symbols[i + (pagenumber - 1)*len(symbolslist)] = s
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
        year = year - 1
