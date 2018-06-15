# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 10:46:00 2018

@author: Administrator
"""

from lottery_possion import * 
import pandas as pd

#用2010年ratio,回测2014年世界杯结果
year = 2014
Asia_Country = [u'伊朗',u'日本',u'韩国',u'澳大利亚']
Africa_Country = [u'加纳',u'科特迪瓦',u'尼日利亚',u'喀麦隆',u'阿尔及利亚']
NorthAmerica_Country = [u'墨西哥',u'美国',u'洪都拉斯',u'哥斯达黎加']
SouthAmerica_Country = [u'厄瓜多尔',u'乌拉圭',u'阿根廷',u'智利',u'哥伦比亚']
Europe_Country = [u'意大利',u'荷兰',u'德国',u'比利时',u'瑞士',u'英格兰',u'西班牙',u'波黑',u'俄罗斯',
                  u'希腊',u'克罗地亚',u'法国',u'葡萄牙']
CountryList = [Asia_Country, Africa_Country, NorthAmerica_Country, SouthAmerica_Country, Europe_Country]                  
precentralList = ['Precentral_Asia','Precentral_Africa','Precentral_North_America','Precentral_South_America','Precentral_Europe'] 
#ratio = [0.78787878787878785, 0.42777777777777776, 0.43750000000000006, 0.94285714285714273, 0.51506644207374142]
#ratio = [0.5,0.5,0.8,1,1]
#ratio1 = [0.4, 0.5, 0.6, 1, 0.8]

ratio1 = [0.4,0.7,0.7,1,1]
ratio2 = [2,1.3,1,0.5,1]
'''
ratio1 = [0.77,1,0.55,0.6,10.3]
ratio2 = [3.7,1,3.5,5,6]
'''
precentral_goals_scored_list = []
precentral_goals_scored_worldcup_list = []
for j,continent in enumerate(precentralList):
    sql_cmd = "SELECT * FROM " + continent + str(year)
    df = get_data(sql_cmd)
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
    #total_df.to_csv('C:/Users/Administrator/Desktop/lottery2014.csv',encoding='gbk')
advantages_index,mean_host_win,mean_guest_win,hit_lose_ball = data_analysis(total_df)
expected_host_ball_set, expected_guest_ball_set = expected_hitball_number(advantages_index,mean_host_win,mean_guest_win)
df_score_probability, df_win_lose_probability = ballprobability(expected_host_ball_set,expected_guest_ball_set) 
save_probability_to_sql(df_win_lose_probability, 'worldcup_win_lose_probability'+str(year))

finished_matches = get_data("SELECT * FROM worldcup_dataildata2014")
correct_ratio,count = calculate_correct_ratio(finished_matches, df_win_lose_probability,df_score_probability, 1)


'''
year = 2010
Asia_Country = [u'朝鲜',u'日本',u'韩国',u'澳大利亚']
Africa_Country = [u'加纳',u'科特迪瓦',u'尼日利亚',u'喀麦隆',u'阿尔及利亚']
NorthAmerica_Country = [u'墨西哥',u'美国',u'洪都拉斯']
SouthAmerica_Country = [u'巴西',u'乌拉圭',u'阿根廷',u'智利',u'巴拉圭']
Europe_Country = [u'荷兰',u'英格兰',u'西班牙',u'德国',u'丹麦',u'塞尔维亚',u'意大利',u'瑞士',
                  u'斯洛伐克',u'法国',u'希腊',u'葡萄牙',u'斯洛文尼亚']
CountryList = [Asia_Country, Africa_Country, NorthAmerica_Country, SouthAmerica_Country, Europe_Country]                  
precentralList = ['Precentral_Asia','Precentral_Africa','Precentral_North_America','Precentral_South_America','Precentral_Europe'] 
#ratio1 = [0.78787878787878785, 0.42777777777777776, 0.43750000000000006, 0.94285714285714273, 0.51506644207374142]
#ratio1 = [0.5, 0.5, 0.8, 1, 1]

ratio1 = [0.4,0.4,0.7,0.7,1,1]
ratio2 = [2,1.3,1,0.5,1]


precentral_goals_scored_list = []
precentral_goals_scored_worldcup_list = []
for j,continent in enumerate(precentralList):
    sql_cmd = "SELECT * FROM " + continent + str(year)
    df = get_data(sql_cmd)
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
    #total_df.to_csv('C:/Users/Administrator/Desktop/lottery2010.csv',encoding='gbk')
advantages_index,mean_host_win,mean_guest_win,hit_lose_ball = data_analysis(total_df)
expected_host_ball_set, expected_guest_ball_set = expected_hitball_number(advantages_index,mean_host_win,mean_guest_win)
df_score_probability, df_win_lose_probability = ballprobability(expected_host_ball_set,expected_guest_ball_set) 

finished_matches = get_data("SELECT * FROM worldcup_dataildata2010")
correct_ratio,count = calculate_correct_ratio(finished_matches, df_win_lose_probability,df_score_probability, 1)
'''