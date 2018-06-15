# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 13:26:40 2018

@author: Administrator
"""
import MySQLdb
import pandas as pd
from itertools import combinations
import numpy as np
import scipy.stats as st
import copy
from lottery_possion import * 

'''将参加世界杯的32只球队的数据筛选出来'''
Asia_Country = [u'伊朗',u'日本',u'韩国',u'沙特',u'澳大利亚']
Africa_Country = [u'埃及',u'尼日利亚',u'突尼斯',u'塞内加尔',u'摩洛哥']
NorthAmerica_Country = [u'墨西哥',u'哥斯达黎加',u'巴拿马']
SouthAmerica_Country = [u'巴西',u'乌拉圭',u'阿根廷',u'哥伦比亚',u'秘鲁']
Europe_Country = [u'德国',u'西班牙',u'比利时',u'英格兰',u'波兰',u'冰岛',u'塞尔维亚',
                  u'法国',u'葡萄牙',u'瑞士',u'瑞典',u'克罗地亚',u'丹麦']
CountryList = [Asia_Country, Africa_Country, NorthAmerica_Country, SouthAmerica_Country, Europe_Country]                  
precentralList = ['Precentral_Asia','Precentral_Africa','Precentral_North_America','Precentral_South_America','Precentral_Europe'] 


year = 2018
ratio1 = [0.4,0.7,0.7,1,1]
ratio2 = [2,1.3,1,0.5,1]
'''提取参加世界杯球队的数据(预选赛)，并将进球数、失球数标准化'''
for j,continent in enumerate(precentralList):
    sql_cmd = "SELECT * FROM " + continent +str(year)
    df = get_data(sql_cmd)
    #选出球队
    new_df = df.loc[df['Team'].isin(CountryList[j])]
    new_df['host_goals_scored'] = new_df['goals_scored'] * ratio1[j]      
    new_df['guest_goals_scored'] = new_df['goals_scored'] * ratio1[j]   
    new_df['host_goals_against'] = new_df['goals_against'] * ratio2[j]      
    new_df['guest_goals_against'] = new_df['goals_against'] * ratio2[j]   
    new_df['host_game_num'] = new_df['game_num'] 
    new_df['guest_game_num'] = new_df['game_num']         

    if j == 0 :
        total_df = new_df
    else:
        total_df = pd.merge(new_df,total_df, how='outer')
    #total_df.to_csv('C:/Users/Administrator/Desktop/lottery2018.csv',encoding='gbk')
#计算进攻优势、防守优势
advantages_index,mean_host_win,mean_guest_win,hit_lose_ball = data_analysis(total_df)
#计算期望进球数
expected_host_ball_set, expected_guest_ball_set = expected_hitball_number(advantages_index,mean_host_win,mean_guest_win)
#计算胜平负概率，并保存在数据库中
df_score_probability, df_win_lose_probability = ballprobability(expected_host_ball_set,expected_guest_ball_set) 
save_probability_to_sql(df_win_lose_probability, 'worldcup_win_lose_probability'+str(year))
#读取今天可以下注的比赛
today_match_csv = 'C:/Users/Administrator/Desktop/yingchao_season_score/jingcai_today_data.csv'    
today_matches =pd.read_csv(today_match_csv,header = 0,encoding='gbk')

#找出可以投注的比赛
today_matches = today_matches.loc[today_matches['score'].isnull() == True]
today_matches['Team'] = today_matches['host'] + today_matches['guest']
today_matches = today_matches.reset_index(drop=True)

#对今日的比赛场次进行预测
today_match_predict = today_match_prediction(today_matches,year)
    