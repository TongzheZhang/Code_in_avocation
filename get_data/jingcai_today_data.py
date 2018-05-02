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
    symbols[j] = s
df_symbols = pd.DataFrame(symbols).T
df_symbols.to_csv('C:/Users/Administrator/Desktop/yingchao_season_score/jingcai_today_data.csv',encoding='gbk')


      

'''
    div = table.select('div')
    p = table.select('p class')
    s['liansai'] = p[0].text
    s['host'] = div[8].text
    s['host_score'] = div[9].text

'''
'''
    p = table.select('p')
    s['liansai'] = p[0].text
    symbols[j] = s
    j = j+1
print symbols       
'''             
'''
        symbolslist = table.select('tr')[1:]
        for symbol in symbolslist:
            tds = symbol.select('td')
            s = {}
            
            s['time'] = tds[0].text  # Time
            s['round'] = tds[1].text  # 第几轮    
            s['host'] = tds[2].text  # Host
            s['score'] = tds[3].text  # 比分            
            s['guest'] = tds[4].text  # Guest
            s['chupei_win'] = tds[5].text  # 赔率
            s['chupei_draw'] = tds[6].text  # 赔率
            s['chupei_lose'] = tds[7].text  # 赔率     
            #symbols[i + (pagenumber - 1)*len(symbolslist)] = s
            symbols[j] = s
            j = j + 1           
'''