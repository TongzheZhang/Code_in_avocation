# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 16:15:52 2018

@author: Administrator
"""

import MySQLdb
import pandas as pd
from itertools import combinations
import numpy as np
import scipy.stats as st
import copy
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Float, Integer


#从数据库中得到数据
def get_data(sql_cmd):    
    con = MySQLdb.connect(host='127.0.0.1', user = 'root', passwd = '', db ='zucai', port = 3306, charset = 'utf8', use_unicode=True)
    df = pd.read_sql(sql_cmd, con)
    return df

#将胜平负概率保存在数据库中
def save_probability_to_sql(df_probability, name):
    dtypedict = {
      'draw': Float(),
      'lose': Float(),
      'win': Float()
    }
    
    yconnect = create_engine('mysql+mysqldb://root:@127.0.0.1:3306/zucai?charset=utf8') 
    pd.io.sql.to_sql(df_probability, name, yconnect, schema='zucai', if_exists='replace',dtype=dtypedict)  

#从数据库中提取出有效内容
def read_db(table_name, Team):
    connect=MySQLdb.connect(host='127.0.0.1', db='zucai', user ='root', passwd = '', charset='utf8', use_unicode=False)#指定链接格式为UTF8
    cursors=connect.cursor() #设定游标
    cursors.execute(
        " SELECT * FROM " + table_name + " WHERE CONVERT(`Team` USING utf8) LIKE '%" + Team + "%'")   
    result = cursors.fetchall()
    
    connect.commit() #事务提交  
    cursors.close()
    connect.close()
    return result
        
#计算主客队进攻优势和防守优势
def data_analysis(df): 
    #仅取今年的联赛数据，并设Team为index
    df.set_index(["Team"], inplace=True)
    df_merge_new = copy.copy(df)
    
    df_merge_new['avg_host_goals_scored'] = df_merge_new['host_goals_scored']/df_merge_new['host_game_num']
    df_merge_new['avg_host_goals_against'] = df_merge_new['host_goals_against']/df_merge_new['host_game_num']              
    df_merge_new['avg_guest_goals_scored'] = df_merge_new['guest_goals_scored']/df_merge_new['guest_game_num']
    df_merge_new['avg_guest_goals_against'] = df_merge_new['guest_goals_against']/df_merge_new['guest_game_num']
    mean_host_win = df_merge_new['avg_host_goals_scored'].mean()
    mean_host_lose = df_merge_new['avg_host_goals_against'].mean()      
    mean_guest_win = df_merge_new['avg_guest_goals_scored'].mean()
    mean_guest_lose = df_merge_new['avg_guest_goals_against'].mean()      
    dataset = {}
    dataset['客场进攻优势'.decode('utf8')] = df_merge_new['avg_guest_goals_scored']/mean_guest_win
    dataset['客场防守优势'.decode('utf8')] = df_merge_new['avg_guest_goals_against']/mean_guest_lose
    dataset['主场进攻优势'.decode('utf8')] = df_merge_new['avg_host_goals_scored']/mean_host_win
    dataset['主场防守优势'.decode('utf8')] = df_merge_new['avg_host_goals_against']/mean_host_lose
    data = pd.DataFrame(dataset)     
    #data.to_csv('C:/Users/Administrator/Desktop/yingchao_season_score/%sdata_matrix.csv'%name,encoding='gbk')
    df_merge_new.to_csv('C:/Users/Administrator/Desktop/lottery1.csv',encoding='gbk')
    return data,mean_host_win,mean_guest_win,df_merge_new

#计算期望进球数
def expected_hitball_number(data,mean_host_win,mean_guest_win):
    host_ball_set = {}
    guest_ball_set = {}
    for i in range(len(data)):
        for j in range(len(data)):
            if i <> j: 
                host_ball = data['主场进攻优势'.decode('utf8')].ix[i] *  data['客场防守优势'.decode('utf8')].ix[j] * mean_host_win
                guest_ball = data['客场进攻优势'.decode('utf8')].ix[j] * data['主场防守优势'.decode('utf8')].ix[i] * mean_guest_win
                host_ball_set[data.index[i] + data.index[j]] = host_ball
                guest_ball_set[data.index[i] + data.index[j]] = guest_ball
    return host_ball_set, guest_ball_set

#计算得到各个比分的概率和胜平负的概率
def ballprobability(host_ball_set,guest_ball_set):
    score_probability_set = {}
    win_lose_probability_set = {}
    for i,k in enumerate(host_ball_set.keys()):
        score_probability = {}
        win_lose_probability = {}
        win_probability = 0
        lose_probability = 0
        draw_probability = 0
        for host_scores in range(0,10):
            for guest_scores in range(0,10):
                host_probability = st.poisson.pmf(host_scores,host_ball_set[k])
                guest_probability = st.poisson.pmf(guest_scores,guest_ball_set[k])
                probability = host_probability * guest_probability
                score_probability[str(host_scores)+':'+str(guest_scores)] = probability
                if host_scores > guest_scores:
                    win_probability = win_probability + probability
                if host_scores < guest_scores:
                    lose_probability = lose_probability + probability
                if host_scores == guest_scores:
                    draw_probability = draw_probability + probability
            score_probability_set[k] = score_probability
        win_lose_probability['Team'] = k
        win_lose_probability['win'] = win_probability
        win_lose_probability['draw'] = draw_probability
        win_lose_probability['lose'] = lose_probability
        win_lose_probability_set[i] = win_lose_probability

    cols = ['Team','win','draw','lose']
    df_score_probability = pd.DataFrame(score_probability_set)
    df_win_lose_probability = pd.DataFrame(win_lose_probability_set).T
    df_win_lose_probability = df_win_lose_probability[cols]
    
    return df_score_probability, df_win_lose_probability
    
#计算预测正确的概率，finished_matches为测试的比赛
def calculate_correct_ratio(finished_matches, df_win_lose_probability,df_score_probability, mode):
    if mode == 1: #计算胜平负正确率
        count_correct = 0
        count = 0
        for i, match in enumerate(finished_matches['Team']):
            len_key = len(df_win_lose_probability.loc[df_win_lose_probability['Team'] == match])
            if len_key == 1:
                count = count + 1
                info = df_win_lose_probability.loc[df_win_lose_probability['Team'] == match]
                del(info['Team'])
                info = info.reset_index(drop=True)
                if np.argmax(info.ix[0]) == finished_matches['result'].ix[i]:
                    count_correct = count_correct + 1
            else:
                pass
        correct_ratio = float(count_correct)/count
        
    if mode == 2:  #计算猜比分正确率
        count_correct = 0
        count = 0
        for i, match in enumerate(finished_matches['Team']):
            try:
                df_score_probability[match]
            except KeyError:
                pass
            else:
                count = count + 1
                if np.argmax(df_score_probability[match]) == str(finished_matches['host_score'].ix[i])+':'+ str(finished_matches['guest_score'].ix[i]):
                    count_correct = count_correct + 1
        correct_ratio = float(count_correct)/count
    return correct_ratio,count
    
#统计当日比赛胜平负概率    
def today_match_prediction(today_matches,year):
    liansai_list = [u'世界杯',u'英超']
    table_name_list = ['worldcup','yingchao']
    prob_set = {}
    for i in range(len(today_matches)):    
        prob = {}
        #在数据库中查找每场比赛的胜平负概率
        try:
            loc=liansai_list.index(today_matches.ix[i]['liansai'])
            table = table_name_list[loc]
            table_name = table +'_win_lose_probability'+str(year)
            result = read_db(table_name, today_matches.ix[i]['Team']) 
            if len(result) > 0:
                prob['win_prob'] = result[0][2]
                prob['draw_prob'] = result[0][3]
                prob['lose_prob'] = result[0][4]
            else:
                prob['win_prob'] = 'Not Predicted'
                prob['draw_prob'] = 'Not Predicted'
                prob['lose_prob'] = 'Not Predicted'
        except ValueError:
            prob['win_prob'] = 'Not Predicted'
            prob['draw_prob'] = 'Not Predicted'
            prob['lose_prob'] = 'Not Predicted'
        
        prob_set[i] = prob
    df_prob_set = pd.DataFrame(prob_set).T
    today_matches_prediction = pd.DataFrame.join(today_matches, df_prob_set)
    col_left = ['time','host','guest','peilv_win','peilv_draw','peilv_lose','win_prob','draw_prob','lose_prob']
    today_matches_prediction_new = today_matches_prediction[col_left]
    today_matches_prediction_new.rename(columns={'time': u'赛事', 'host': u'主队', 'guest': u'客队', 'peilv_win': u'赔率（胜）', 
                                                 'peilv_draw': u'赔率（平）','peilv_lose': u'赔率（负）','win_prob': u'概率（胜）',
                                                 'draw_prob': u'概率（平）','lose_prob': u'概率（负）'}, inplace=True) 
    today_matches_prediction_new.to_csv('C:/Users/Administrator/Desktop/todaymatch_prediction.csv',encoding='gbk')   
    return today_matches_prediction_new
     
#计算2串1、3串1的盈利期望，其中today_matches_fiveLeague为要预测的比赛
def profit_expectation(df_score_probability, df_win_lose_probability,today_matches_fiveLeague,mode):
    expected_profit_set = {}
    if mode == 1: #2串1
        if len(today_matches_fiveLeague)<2:
            print('The chosen group is less than expected.')
        else:
            elements = list(combinations(range(len(today_matches_fiveLeague)), 2))
            #total_expected_profit = 0
            i = 0
            for group_num in elements:
                expected_profit_ele = {}
                try:
                    matchgroup1 = today_matches_fiveLeague['Team'].ix[group_num[0]]
                    matchliansai1 = today_matches_fiveLeague['liansai'].ix[group_num[0]]
                    a = df_win_lose_probability[matchliansai1].loc[matchgroup1]
    
                    matchgroup2 = today_matches_fiveLeague['Team'].ix[group_num[1]]
                    matchliansai2 = today_matches_fiveLeague['liansai'].ix[group_num[1]]
                    b = df_win_lose_probability[matchliansai2].loc[matchgroup2]
    
                    peilv_a = today_matches_fiveLeague['peilv_' + np.argmax(a)].ix[group_num[0]]
                    peilv_b = today_matches_fiveLeague['peilv_' + np.argmax(b)].ix[group_num[1]]
                    expected_profit = max(a) * max(b) * peilv_a * peilv_b - 1
                    if expected_profit > 0 and max(a) > 0.6 and max(b) > 0.6:
                        expected_profit_ele['mode'] = mode
                        expected_profit_ele['expected_profit'] = expected_profit
                        expected_profit_ele['match1'] = matchgroup1
                        expected_profit_ele['match1_result'] = np.argmax(a)
                        expected_profit_ele['match2'] = matchgroup2
                        expected_profit_ele['match2_result'] = np.argmax(b)
                        expected_profit_ele['peilv'] = peilv_a * peilv_b
                        expected_profit_set[i] = expected_profit_ele

                        i = i + 1
                        print mode, expected_profit, matchgroup1,np.argmax(a),matchgroup2,np.argmax(b)
                        print a
                        print b
                except KeyError:
                    pass
            df_expected_profit_set = pd.DataFrame(expected_profit_set).T
            return df_expected_profit_set
            
    if mode == 2: #3串1
        if len(today_matches_fiveLeague)<3:
            print('The chosen group is less than expected.')
        else:
            elements = list(combinations(range(len(today_matches_fiveLeague)), 3))
            #total_expected_profit = 0            
            for group_num in elements:
                try:
                    matchgroup1 = today_matches_fiveLeague['Team'].ix[group_num[0]]
                    matchliansai1 = today_matches_fiveLeague['liansai'].ix[group_num[0]]
                    a = df_win_lose_probability[matchliansai1].loc[matchgroup1]
    
                    matchgroup2 = today_matches_fiveLeague['Team'].ix[group_num[1]]
                    matchliansai2 = today_matches_fiveLeague['liansai'].ix[group_num[1]]
                    b = df_win_lose_probability[matchliansai2].loc[matchgroup2]
    
                    matchgroup3 = today_matches_fiveLeague['Team'].ix[group_num[2]]
                    matchliansai3 = today_matches_fiveLeague['liansai'].ix[group_num[2]]
                    c = df_win_lose_probability[matchliansai3].loc[matchgroup3]
                    #print elements[group_num][0], np.argmax(a),max(a),elements[group_num][1], np.argmax(b),max(b),
                    peilv_a = today_matches_fiveLeague['peilv_' + np.argmax(a)].ix[group_num[0]]
                    peilv_b = today_matches_fiveLeague['peilv_' + np.argmax(b)].ix[group_num[1]]
                    peilv_c = today_matches_fiveLeague['peilv_' + np.argmax(c)].ix[group_num[2]]
                                                       
                    expected_profit = max(a) * max(b) * max(c) * peilv_a * peilv_b * peilv_c - 1
                    if expected_profit > 0.2 and max(a) > 0.5 and max(b) > 0.5 and max(c) > 0.5:
                        print mode, expected_profit, matchgroup1,np.argmax(a),matchgroup2,np.argmax(b),matchgroup3,np.argmax(c)   
                except KeyError:
                    pass
