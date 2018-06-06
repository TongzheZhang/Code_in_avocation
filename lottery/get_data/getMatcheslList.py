# -*- coding: utf-8 -*-
"""
Created on Thu May 31 13:48:24 2018

@author: Administrator
"""
import urllib 
from bs4 import BeautifulSoup
import pandas as pd
import re
from sqlalchemy import create_engine 
from sqlalchemy.types import NVARCHAR, Float, Integer
import requests
import json

yearList = [2017,2018]
monList = range(1,13)
matchIDList = []
for year in yearList:
    for mon in monList:
        if mon == 1 or mon == 3 or mon == 5 or mon == 7 or mon == 8 or mon == 10 or mon == 12:
            day = 31
            mon = str(mon).zfill(2)
            year = str(year).zfill(2)
            day = str(day).zfill(2)
    
        if mon == 2 or mon == 4 or mon == 6 or mon == 9 or mon == 11:
            day = 30
            mon = str(mon).zfill(2)
            year = str(year).zfill(2)
            day = str(day).zfill(2)
            
        startDay = year+'.'+mon+'.'+'01'
        endDay = year+'.'+mon+'.'+day
        #print startDay, endDay

        #url = "http://www.tzuqiu.cc/matches/queryFixture.json?comeptitionId=1&date=%s+\%E8+%s"%(startDay,endDay)
        url = "http://www.tzuqiu.cc/matches/queryFixture.json?comeptitionId=1&date="+startDay+"+%E8%87%B3+"+endDay
        pageSource = requests.get(url).text
        text = json.loads(pageSource)
        matchInfo = text['datas']
        for each in matchInfo:
            matchID = each['id']
            matchIDList.append(matchID)
file = open('C:/Users/Administrator/Desktop/yingchao_season_score/MatchIDList.txt','w')  
file.write(str(matchIDList)) 
file.close()  

            
        




         
