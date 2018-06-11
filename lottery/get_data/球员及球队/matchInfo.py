# -*- coding: utf-8 -*-
"""
Created on Wed May 30 11:22:10 2018

@author: Administrator
"""

from bs4 import BeautifulSoup
import pandas as pd
import re
from sqlalchemy import create_engine 
from sqlalchemy.types import NVARCHAR, Float, Integer
import requests
import json

file = open('C:/Users/Administrator/Desktop/yingchao_season_score/MatchIDList.txt','r')  
matchIDList = file.read()
file.close()
matchIDList = eval(matchIDList) #将str还原为list

symbols = {}
for matchNum,matchID in enumerate(matchIDList[0:10]):
    url = "http://www.tzuqiu.cc/matches/"+str(matchID)+"/stat.do"
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh-CN',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.2.2.2000',
               'Referer': url
               }

    pageSource = requests.get(url).text
    html_parse = BeautifulSoup(pageSource)
    
    s ={}
    summary_header_result = html_parse.findAll('div',{'id':'match-summary-header-result'})[0] 
    s['score'] = summary_header_result.findAll('div',{'class':'macth-score'})[0].text
    
    summary_header_team_host = html_parse.findAll('div',{'class':'match-summary-header-team-info'})[0] 
    s['host'] = summary_header_team_host.findAll('a',{'class':'team-name home-color'})[0].text
    summary_header_team_guest = html_parse.findAll('div',{'class':'match-summary-header-team-info'})[1] 
    s['away'] = summary_header_team_guest.findAll('a',{'class':'team-name away-color'})[0].text
    s['matchID'] = matchID
    #print html_parse
    
    reObj_home = re.match(".*?homePlayerStatistics = (.*?);", str(html_parse).replace('\r','').replace('\n',''))
    a = reObj_home.group(1)
    text_home = json.loads(a)
    reObj_away = re.match(".*?awayPlayerStatistics = (.*?);", str(html_parse).replace('\r','').replace('\n',''))
    b = reObj_away.group(1)
    text_away = json.loads(b)
    
    symbol_home = {}
    for num, player in enumerate(text_home[0:11]):
        player_s = {}
        player_s['player_id'] = player['id'] 
        player_s['player_name'] = player['playerName']
        player_s['shirtNo'] = player['shirtNo'] 
        symbol_home[num] = player_s
    
    symbol_away = {}
    for num, player in enumerate(text_away[0:11]):
        player_s = {}
        player_s['player_id'] = player['id'] 
        player_s['player_name'] = player['playerName']
        player_s['shirtNo'] = player['shirtNo'] 
        symbol_away[num] = player_s
    
    for i in range(0,11):
        s['host_player'+str(i)] = symbol_home[i]
        s['away_player'+str(i)] = symbol_away[i]  
    symbols[matchNum] = s
    df = pd.DataFrame(s).T
df1 = pd.DataFrame(symbols).T


