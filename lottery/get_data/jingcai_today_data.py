# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 15:54:50 2018

@author: Administrator
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
from sqlalchemy import create_engine 
from sqlalchemy.types import NVARCHAR, Float, Integer
import json


driver = webdriver.PhantomJS(executable_path = 'D:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
url = "http://www.okooo.com/jingcai/"
#爬取数据（比赛场次，比分，赔率等）
driver.get(url)
pageSource = driver.page_source
        
html_parse = BeautifulSoup(pageSource)
table_set = html_parse.findAll('div',{'class':'touzhu_1'})
symbols = {}
for j,table in enumerate(table_set): 
    s = {}
    #print table
    #s['host'] = table.findAll('div',{'class':'zhum fff hui_colo'})
    s['ID'] = table.select('span')[0].text
    s['time'] = table.select('span')[0]['title']

    s['match_num'] = table['data-mid']
    liansai = table.select('.saiming.aochao')
    s['liansai'] = liansai[0].text
    team = table.select('div .zhum.fff.hui_colo ')
    s['host'] = team[0].text
    s['guest'] = team[1].text
    peilv = table.select('div .peilv.fff.hui_colo.red_colo')
    s['peilv_win'] = peilv[0].text
    s['peilv_draw'] = peilv[1].text
    s['peilv_lose'] = peilv[2].text
    s['rang_peilv_win'] = peilv[3].text
    s['rang_peilv_draw'] = peilv[4].text
    s['rang_peilv_lose'] = peilv[5].text
    try:
        rangqiu_num = table.select('.rangqiu')
        s['rangqiu_num'] = rangqiu_num[0].text
    except IndexError:
        rangqiu_num = table.select('.rangqiuzhen')
        s['rangqiu_num'] = rangqiu_num[0].text


    score = table.select('.p1')
    try:
        s['score'] = score[-1].text
    except IndexError:
        score = table.select('.p1.count')
        s['score'] = score[-1].text       
 
    try:
        danguan = table.select('div .danguan') 
        if danguan <> []:
            s['danguan'] = 'danguan'
    except IndexError:
        pass
    
    #根据matchID爬取初赔(bet365)
    url_startodds = 'http://www.okooo.com/I/?method=lottery.match.oddschangeline&pid=27&limit=3&isReversion=N&matchId=%s&format=json&bid=1'%s['match_num']
    driver.get(url_startodds)
    pageSource = driver.page_source
    html_parse = BeautifulSoup(pageSource)
    a = html_parse.text
    
    text = json.loads(a)
    b = text['match_oddschangeline_response']
    c = b['oddsList']    
    startOdds = c['start']['odds']
    s['startOdds_bet365_win'] = startOdds[0]
    s['startOdds_bet365_draw'] = startOdds[1]
    s['startOdds_bet365_lose'] = startOdds[2]
    
    #根据matchID爬取初赔(libo)
    url_startodds = 'http://www.okooo.com/I/?method=lottery.match.oddschangeline&pid=82&limit=3&isReversion=N&matchId=%s&format=json&bid=1'%s['match_num']
    driver.get(url_startodds) 
    pageSource = driver.page_source
    html_parse = BeautifulSoup(pageSource)
    a = html_parse.text   
    text = json.loads(a)
    b = text['match_oddschangeline_response']
    c = b['oddsList']    
    try:
        startOdds = c['start']['odds']
        s['startOdds_libo_win'] = startOdds[0]
        s['startOdds_libo_draw'] = startOdds[1]
        s['startOdds_libo_lose'] = startOdds[2]
    except TypeError:
        pass

    symbols[j] = s
df_symbols = pd.DataFrame(symbols).T
df_symbols.to_csv('C:/Users/Administrator/Desktop/yingchao_season_score/jingcai_today_data.csv',encoding='gbk')



      
