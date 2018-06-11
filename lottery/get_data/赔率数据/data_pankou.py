# -*- coding: utf-8 -*-
"""
Created on Mon May 07 10:15:05 2018

@author: Administrator
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import json
import pandas as pd
import re
from sqlalchemy import create_engine 
from sqlalchemy.types import NVARCHAR, Float, Integer
import time

driver = webdriver.PhantomJS(executable_path = 'D:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
for year in range(2017,2018):
    for i1 in range(1,13):
        for i2 in range(1,32):
            mon = str(i1).zfill(2)
            day = str(i2).zfill(2)
            url = "http://odds.500.com/index_history_%s-%s-%s.shtml#!"%(year,mon,day)
            driver.get(url)
            pageSource = driver.page_source
            
            html_parse = BeautifulSoup(pageSource)
            
            table = html_parse.findAll('tbody',{'id':'main-tbody'})[0] 
            
            symbolslist = table.select('tr')[0:]
            j = 0
            symbols = {}
            for symbol in symbolslist:
                if symbol['data-cid'] == '3':   
                    s = {}
                    #s['bocai_company'] = symbol['data-cid']
                    s['match_num'] = symbol['data-fid']
                    tds = symbol.select('td')
                    s['competition'] = tds[1].text
                    s['time'] = tds[3].text
                    s['host'] = tds[4].text
                    s['score'] = tds[5].text
                    s['guest'] = tds[6].text  
                    #s['company'] = tds[7].text
                    s['level1'] = tds[8].text
                    s['plate'] = tds[9].text
                    s['level2'] = tds[10].text
                    '''
                    s['peilv_win_3'] = tds[11].text
                    s['peilv_draw_3'] = tds[12].text
                    s['peilv_lose_3'] = tds[13].text
                    '''
                    symbols[j] = s
                    j = j + 1           
                else:
                    pass
            df_symbols = pd.DataFrame(symbols).T 
            new_df_symbols = df_symbols.set_index('match_num')
            script = html_parse.findAll('script')[-8] 
            script_new = str(script).replace("\n","").replace("\r","")
            reObj = re.match(".*?ouzhiList=(.*?);", script_new)
            try:
                text = json.loads(reObj.group(1))
                new_text = {}
                for k in text:
                    try:
                        new_text[k] = text[k]['2'][1][0:3]+text[k]['3'][1][0:3]
                        #new_text[k][1] = text[k]['3'][1][0:3]
                    except KeyError:
                        pass
                new_df_text = pd.DataFrame(new_text).T
                new_df_text.columns = ['peilv_win_2','peilv_draw_2','peilv_lose_2','peilv_win_3','peilv_draw_3','peilv_lose_3']
                
                data = pd.concat([new_df_symbols,new_df_text],axis = 1)
                data = data.reset_index(drop=False) #index重新定义
                data.rename(columns={"index":"num"},inplace = True
                
                dtypedict = {
                  'guest': NVARCHAR(length=255),
                  'host': NVARCHAR(length=255),
                  'score': NVARCHAR(length=255),
                  'time': NVARCHAR(length=255),
                  'num': Integer(),
                  'competition': NVARCHAR(length=255),
                  'round': Integer(),
                  'host_score': Integer(),
                  'guest_score': Integer()
                }
                  #'level1': Float(),
                  #'plate': Float(),
                  #'level2': Float(),
                  #'peilv_win_3': Float(),
                  #'peilv_draw_3': Float(),
                  #'peilv_lose_3': Float()
                
                
                yconnect = create_engine('mysql+mysqldb://root:@127.0.0.1:3306/zucai?charset=utf8') 
                pd.io.sql.to_sql(data,'pankou_data_%d'%year, yconnect, schema='zucai', if_exists='append',dtype=dtypedict)  
            except ValueError:
                pass
