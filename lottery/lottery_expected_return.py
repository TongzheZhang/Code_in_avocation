# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 11:07:53 2018

@author: Administrator
"""
import MySQLdb
import pandas as pd
from itertools import combinations
import numpy as np
import scipy.stats as st
import copy

'''
connect_info = 'mysql+mysqldb://root:@127.0.0.1:3306/zucai?charset=utf8'
engine = create_engine(connect_info)
# sql 命令
df = pd.read_sql(sql=sql_cmd, con=engine)

'''
def get_data(sql_cmd):    
    con = MySQLdb.connect(host='127.0.0.1', user = 'root', passwd = '', db ='zucai', port = 3306, charset = 'utf8', use_unicode=True)
    df_each_year = pd.read_sql(sql_cmd, con)
    return df_each_year

def data_league(name): #将三年联赛的数据整合起来
    df = []
    for year in range(17,18):
        sql_cmd = "SELECT * FROM %s"%name+str(year)
        df.append(get_data(sql_cmd))
    return df
    
#此函数用来计算各队主客场平均进球、失球数。
def data_analysis(df,name): #df为几届的比赛的数据（4个sheet）
    #将四个表格合并，并以Team为index，进行加和合并。
    '''
    df_merge1 = pd.merge(df[0],df[1],how ='outer')
    df_merge2 = pd.merge(df[2],df_merge1,how ='outer')
    df_merge = pd.merge(df[3],df_merge2,how ='outer')

    df_merge_new = df_merge.groupby(['Team']).sum()
    '''
    #仅取今年的联赛数据，并设Team为index
    df = pd.DataFrame(df[0])
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
    data.to_csv('C:/Users/Administrator/Desktop/yingchao_season_score/%sdata_matrix.csv'%name,encoding='gbk')
    df_merge_new.to_csv('C:/Users/Administrator/Desktop/yingchao_season_score/%sdata_sum.csv'%name,encoding='gbk')
    return data,mean_host_win,mean_guest_win,df_merge_new
 
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

def ballprobability(host_ball_set,guest_ball_set):
    score_probability_set = {}
    win_lose_probability_set = {}
    for k in host_ball_set.keys():
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
        win_lose_probability['win'] = win_probability
        win_lose_probability['draw'] = draw_probability
        win_lose_probability['lose'] = lose_probability
        win_lose_probability_set[k] = win_lose_probability
    
    df_score_probability = pd.DataFrame(score_probability_set)
    df_win_lose_probability = pd.DataFrame(win_lose_probability_set).T
    
    df_win_lose_probability.to_csv('C:/Users/Administrator/Desktop/yingchao_season_score/win_lose_probability.csv',encoding='gbk')
    df_score_probability.to_csv('C:/Users/Administrator/Desktop/yingchao_season_score/df_score_probability.csv',encoding='gbk')
    return df_score_probability, df_win_lose_probability
    
def calculate_correct_ratio(finished_matches, df_win_lose_probability,df_score_probability, mode):
    if mode == 1: #计算胜平负正确率
        count_correct = 0
        count = 0
        for i, match in enumerate(finished_matches['Team']):
            try:
                df_win_lose_probability.loc[match]
            except KeyError:
                pass
            else:
                count = count + 1
                if np.argmax(df_win_lose_probability.loc[match]) == finished_matches['result'].ix[i]:
                    count_correct = count_correct + 1
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

def Filter_today_matches(csv):
    today_matches =pd.read_csv(csv,header = 0,encoding='gbk')
    #找出可以投注的比赛
    today_matches = today_matches.loc[today_matches['score'].isnull() == True]
    today_matches['Team'] = today_matches['host'] + today_matches['guest']                                 
    #将五大联赛分开                                
    English_Premier_League_Matches = today_matches.loc[today_matches['liansai']=='英超'.decode('utf8')]
    Italy_Serie_A_Matches = today_matches.loc[today_matches['liansai']=='意甲'.decode('utf8')]    
    Spanish_La_Liga_Matches = today_matches.loc[today_matches['liansai']=='西甲'.decode('utf8')]         
    German_Bundesliga_Matches = today_matches.loc[today_matches['liansai']=='德甲'.decode('utf8')]    
    France_Ligue_one_Matches = today_matches.loc[today_matches['liansai']=='法甲'.decode('utf8')]
    '''                                             
    K_League_Matches = today_matches.loc[today_matches['liansai']=='K联赛'.decode('utf8')]                                                 
    J_League_Matches = today_matches.loc[today_matches['liansai']=='J联赛'.decode('utf8')]                                                 
    France_Ligue_two_Matches = today_matches.loc[today_matches['liansai']=='法乙'.decode('utf8')]                                                 
    German_B_Matches = today_matches.loc[today_matches['liansai']=='德甲'.decode('utf8')]  
    '''                                               
                                                 
    English_Premier_League_Matches['liansai'] = 'English_Premier_League'
    Italy_Serie_A_Matches['liansai'] = 'Italy_Serie_A'
    Spanish_La_Liga_Matches['liansai'] = 'Spanish_La_Liga'
    German_Bundesliga_Matches['liansai'] = 'German_Bundesliga'
    France_Ligue_one_Matches['liansai'] = 'France_Ligue_one'
    '''
    K_League_Matches['liansai'] = 'K_League'
    J_League_Matches['liansai'] = 'J_League'
    France_Ligue_two_Matches['liansai'] = 'France_Ligue_two'
    German_B_Matches['liansai'] = 'German_B'
    '''
    '''
    today_matches_fiveLeague = English_Premier_League_Matches.append([Italy_Serie_A_Matches,Spanish_La_Liga_Matches,
                                                                      German_Bundesliga_Matches,France_Ligue_one_Matches,
                                                                      K_League_Matches,J_League_Matches,France_Ligue_two_Matches,
                                                                      German_B_Matches])
    '''
    today_matches_fiveLeague = English_Premier_League_Matches.append([Italy_Serie_A_Matches,Spanish_La_Liga_Matches,
                                                                      German_Bundesliga_Matches,France_Ligue_one_Matches])
                                                                      
    today_matches_fiveLeague = today_matches_fiveLeague.reset_index(drop=True) #index重新定义
    df2_set = {}
    for i in range(len(today_matches_fiveLeague)):
        df2 = {}
        try:
            a = today_matches_fiveLeague['liansai'].ix[i]
            b = today_matches_fiveLeague['Team'].ix[i]
            df2['host_win'] = df_win_lose_probability[a]['win'][b]
            df2['host_draw'] = df_win_lose_probability[a]['draw'][b]
            df2['host_lose'] = df_win_lose_probability[a]['lose'][b]
            df2_set[i] = df2

        except KeyError:
            df2['host_win'] = 'Not Predicted'
            df2['host_draw'] = 'Not Predicted'
            df2['host_lose'] = 'Not Predicted'
            df2_set[i] = df2

    dataframe2 = pd.DataFrame(df2_set).T
    today_matches_fiveLeague_new = today_matches_fiveLeague.join(dataframe2)
    today_matches_fiveLeague_new.to_csv('C:/Users/Administrator/Desktop/today_matches_fiveLeague_new.csv',encoding='gbk')

    return today_matches_fiveLeague                    
    
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
                    
                #total_expected_profit = total_expected_profit + expected_profit
            #print total_expected_profit         
            #return total_expected_profit
    '''
    if mode == 3: #3串4
        total_expected_profit1 = profit_expectation(df_score_probability, df_win_lose_probability,games,1)
        total_expected_profit2 = profit_expectation(df_score_probability, df_win_lose_probability,games,2)
        total_expected_profit = total_expected_profit1 + total_expected_profit2
        print total_expected_profit
        return total_expected_profit
    '''
    
if __name__ == "__main__":    
    '''
    namelist = ['English_Premier_League','Italy_Serie_A','Spanish_La_Liga','German_Bundesliga','France_Ligue_one',
    'J_League','K_League','France_Ligue_two','German_B']  
    '''
    namelist = ['English_Premier_League','Italy_Serie_A','Spanish_La_Liga','German_Bundesliga','France_Ligue_one','Japanese']

    mode = 1
    advantages_index = {}
    mean_host_win = {}
    mean_guest_win = {}
    hit_lose_ball = {}
    expected_host_ball_set = {}
    expected_guest_ball_set = {}
    df_score_probability = {}
    df_win_lose_probability = {}
    finished_matches = {}
    correct_ratio = {}
    count = {}
    for i, name in enumerate(namelist):
        df = data_league(name)
        advantages_index[name],mean_host_win[name],mean_guest_win[name],hit_lose_ball[name] = data_analysis(df,name)
        expected_host_ball_set[name], expected_guest_ball_set[name] = expected_hitball_number(advantages_index[name],mean_host_win[name],mean_guest_win[name])
        df_score_probability[name], df_win_lose_probability[name] = ballprobability(expected_host_ball_set[name],expected_guest_ball_set[name]) 
        finished_matches[name] = get_data("SELECT * FROM %s_recent_matches"%name)
        correct_ratio[name],count[name] = calculate_correct_ratio(finished_matches[name], df_win_lose_probability[name],df_score_probability[name], mode)
    #today_match_csv = 'C:/Users/Administrator/Desktop/yingchao_season_score/jingcai_today_data.csv'    
    #today_matches_fiveLeague = Filter_today_matches(today_match_csv)
    #df_expected_profit_set = profit_expectation(df_score_probability, df_win_lose_probability,today_matches_fiveLeague,1)
