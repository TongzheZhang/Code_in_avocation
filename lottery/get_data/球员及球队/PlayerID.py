# -*- coding: utf-8 -*-
"""
Created on Mon May 28 10:41:43 2018

@author: Administrator
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import json
import pandas as pd
import re
from sqlalchemy import create_engine 
from sqlalchemy.types import NVARCHAR, Float, Integer


driver = webdriver.PhantomJS(executable_path = 'D:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
PlayerIDList = []

for i in range(226):
    url = "https://sofifa.com/players?offset=%d"%(i*80)
    driver.get(url)
    pageSource = driver.page_source
    html_parse = BeautifulSoup(pageSource)
    table = html_parse.findAll('table',{'class':'table table-hover persist-area'})[0] 
    symbolslist = table.select('tr')[3:]
    for symbol in symbolslist:
        #PlayerID = symbol.findAll('div',{'class':'col-array col-pi'})[0]
        '''
        td = symbol.select('td #pi')[0]
        ID = td.select('div .col-array.col-pi')
        PlayerID = ID[0].text
        '''
        figure = symbol.select('img')[0]
        PlayerID = figure['id']
        PlayerIDList.append(PlayerID)
#print PlayerIDList

file = open('C:/Users/Administrator/Desktop/yingchao_season_score/PlayerIDList.txt','w')  
file.write(str(PlayerIDList)) 
file.close()  


