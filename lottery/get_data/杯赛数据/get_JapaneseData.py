# -*- coding: utf-8 -*-
"""
Created on Wed May 16 11:25:32 2018

@author: Administrator
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
from sqlalchemy import create_engine 
from sqlalchemy.types import NVARCHAR, Float, Integer

driver = webdriver.PhantomJS(executable_path = 'D:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
urllist = ["http://www.okooo.com/soccer/league/101/schedule/13686/1-",
           "http://www.okooo.com/soccer/league/101/schedule/13107/1-"]

year = 18
for url in urllist:
    for pagenumber in range(5755,5759):
        driver.get(url + unicode(pagenumber))
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
        pd.io.sql.to_sql(df_symbols, 'Japanese'+str(year), yconnect, schema='zucai', if_exists='append',dtype=dtypedict)  
    year = year - 1


