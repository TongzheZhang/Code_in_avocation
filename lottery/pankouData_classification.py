# -*- coding: utf-8 -*-
"""
Created on Tue May 08 15:09:35 2018

@author: Administrator
"""

import MySQLdb
import pandas as pd
from itertools import combinations
import numpy as np
import scipy.stats as st
from sklearn.linear_model import LinearRegression
#from sklearn.cross_validation import KFold #交叉验证库，将测试集进行切分交叉验证取平均  
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier  
from imblearn.over_sampling import SMOTE, ADASYN
from collections import Counter
from imblearn.combine import SMOTEENN
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier  
  


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


#数据清洗，去掉无比分、无赔率的行，并将result以0,0.5,1的形式表示
def data_clean(data18):
    #去掉无比分的行
    indexs = list(data18[data18['score']=='VS'].index)
    data18_new = data18.drop(indexs)
    data18_new = data18_new.reset_index(drop=True) #index重新定义
    
    scores = data18_new['score'] 
    new_scores = scores.str.split(':',expand = True) #去除比分中的“-”
    
    data18_new['host_score'] = new_scores.ix[:,0]  
    data18_new['guest_score'] = new_scores.ix[:,1]                      

    data18_new['result'] = 0
    indexs = list(data18_new[data18_new['host_score'] > data18_new['guest_score']].index)
    data18_new['result'].ix[indexs] = 1

    indexs = list(data18_new[data18_new['host_score'] == data18_new['guest_score']].index)
    data18_new['result'].ix[indexs] = 0

    indexs = list(data18_new[data18_new['host_score'] < data18_new['guest_score']].index)
    data18_new['result'].ix[indexs] = -1
    
    data18_new[['peilv_win_3','peilv_draw_3','peilv_lose_3']] = data18_new[['peilv_win_3','peilv_draw_3','peilv_lose_3']].apply(pd.to_numeric)
    data18_new[['peilv_win_2','peilv_draw_2','peilv_lose_2']] = data18_new[['peilv_win_2','peilv_draw_2','peilv_lose_2']].apply(pd.to_numeric)

    indexs = list(data18_new[np.isnan(data18_new['peilv_win_3'])].index)
    data18_Bet365 = data18_new.drop(indexs)
    data18_Bet365 = data18_Bet365.reset_index(drop=True) #index重新定义
    data18_Bet365['sum_peilvBet365'] = data18_Bet365['peilv_win_3'] + data18_Bet365['peilv_draw_3'] + data18_Bet365['peilv_lose_3']
    data18_Bet365['nor_peilv_win_3'] = data18_Bet365['peilv_win_3']/data18_Bet365['sum_peilvBet365']
    data18_Bet365['nor_peilv_draw_3'] = data18_Bet365['peilv_draw_3']/data18_Bet365['sum_peilvBet365']
    data18_Bet365['nor_peilv_lose_3'] = data18_Bet365['peilv_lose_3']/data18_Bet365['sum_peilvBet365']


    indexs = list(data18_Bet365[np.isnan(data18_Bet365['peilv_win_2'])].index)
    data18_libo = data18_Bet365.drop(indexs)
    data18_libo = data18_libo.reset_index(drop=True) #index重新定义
    data18_libo['sum_peilvlibo'] = data18_libo['peilv_win_2'] + data18_libo['peilv_draw_2'] + data18_libo['peilv_lose_2']
    data18_libo['nor_peilv_win_2'] = data18_libo['peilv_win_2']/data18_libo['sum_peilvlibo']
    data18_libo['nor_peilv_draw_2'] = data18_libo['peilv_draw_2']/data18_libo['sum_peilvlibo']
    data18_libo['nor_peilv_lose_2'] = data18_libo['peilv_lose_2']/data18_libo['sum_peilvlibo']

    return data18_Bet365, data18_libo

def standard_todaymatches():
    today_matches =pd.read_csv('C:/Users/Administrator/Desktop/yingchao_season_score/jingcai_today_data.csv',header = 0,encoding='gbk')
    today_matches[['peilv_win_3','peilv_draw_3','peilv_lose_3']] = today_matches[['startOdds_bet365_win','startOdds_bet365_draw','startOdds_bet365_lose']].apply(pd.to_numeric)
    today_matches[['peilv_win_2','peilv_draw_2','peilv_lose_2']] = today_matches[['startOdds_libo_win','startOdds_libo_draw','startOdds_libo_lose']].apply(pd.to_numeric)

    indexs = list(today_matches[np.isnan(today_matches['peilv_win_2'])].index)
    today_matches_new = today_matches.drop(indexs)
    today_matches_new = today_matches_new.reset_index(drop=True) #index重新定义
    today_matches_new['sum_peilvBet365'] = today_matches_new['peilv_win_3'] + today_matches_new['peilv_draw_3'] + today_matches_new['peilv_lose_3']
    today_matches_new['nor_peilv_win_3'] = today_matches_new['peilv_win_3']/today_matches_new['sum_peilvBet365']
    today_matches_new['nor_peilv_draw_3'] = today_matches_new['peilv_draw_3']/today_matches_new['sum_peilvBet365']
    today_matches_new['nor_peilv_lose_3'] = today_matches_new['peilv_lose_3']/today_matches_new['sum_peilvBet365']

    today_matches_new['sum_peilvlibo'] = today_matches_new['peilv_win_2'] + today_matches_new['peilv_draw_2'] + today_matches_new['peilv_lose_2']
    today_matches_new['nor_peilv_win_2'] = today_matches_new['peilv_win_2']/today_matches_new['sum_peilvlibo']
    today_matches_new['nor_peilv_draw_2'] = today_matches_new['peilv_draw_2']/today_matches_new['sum_peilvlibo']
    today_matches_new['nor_peilv_lose_2'] = today_matches_new['peilv_lose_2']/today_matches_new['sum_peilvlibo']
    return today_matches_new

    
def balanced_data(data, predictors, method):
    X = np.array(data[predictors])
    y = np.array(data['result'])
    print Counter(y)
    X_resampled, y_resampled = method.fit_sample(X, y)
    print Counter(y_resampled)
    
    data_new = pd.DataFrame(X_resampled, columns=predictors)
    data_new['result'] = y_resampled
    return data_new
    

#Linear Regression, data为处理过的数据，predictors为输入因子
def linearRegressionMethod(data,predictors):
    alg = LinearRegression()
    kf = cross_validation.KFold(data.shape[0],n_folds=3,random_state=1) #将m个样本平均分成3份进行交叉验证  
    
    predictions = []
    for train, test in kf:
        train_predictors = (data[predictors].iloc[train,:])#将predictors作为测试特征  
        train_target = data['result'].iloc[train]  
        alg.fit(train_predictors,train_target)    
        test_prediction = alg.predict(data[predictors].iloc[test,:])  
        predictions.append(test_prediction)         
    predictions = np.concatenate(predictions, axis=0) 
    #alg.fit(data[predictors],data['result'])

    predictions[predictions > 0] = 1  
    predictions[predictions == 0] = 0  
    predictions[predictions <= 0] = -1  
    indexs = predictions == data['result']
    result = indexs.value_counts()
    accuracy = float(result[1]) / len(predictions)#测试准确率  
    print "The accuracy of Linear Regression method is", accuracy           
    return accuracy
    
#Random Forest   
def RandomForestMethod(data,predictors,data2):
    alg = RandomForestClassifier(random_state=1,n_estimators=50,min_samples_split=4,min_samples_leaf=2)  
    '''
    kf = cross_validation.KFold(data.shape[0],n_folds=3,random_state=1)  
    scores = cross_validation.cross_val_score(alg,data[predictors],data['result'],cv=kf)  
    '''
    alg.fit(data[predictors],data['result'])
    scores = alg.score(data2[predictors],data2['result'])
    print "The accuracy of Random Forest method is", scores              
    return scores
#logistic regression, data（均衡化后的数据）用来训练模型，data2（全部数据）用来测试模型
def logisticRegressionMethod(data,predictors,data2):
    alg = LogisticRegression(random_state=1)  
    #scores = cross_validation.cross_val_score(alg, data[predictors],data['result'],cv=3)  
    alg.fit(data[predictors],data['result'])
    scores = alg.score(data2[predictors],data2['result'])
    print "The accuracy of logistic regression method is", scores.mean()    
    return scores.mean()
    
def KNNMethod(data,predictors,data2):
    alg = KNeighborsClassifier()
    alg.fit(data[predictors],data['result'])
    scores = alg.score(data2[predictors],data2['result'])
    print "The accuracy of KNN method is", scores.mean()    
    return scores.mean()

def RandomForestPredict(data,predictors,data2):
    alg = RandomForestClassifier(random_state=1,n_estimators=50,min_samples_split=4,min_samples_leaf=2)  
    '''
    kf = cross_validation.KFold(data.shape[0],n_folds=3,random_state=1)  
    scores = cross_validation.cross_val_score(alg,data[predictors],data['result'],cv=kf)  
    '''
    alg.fit(data[predictors],data['result'])
    y = alg.predict(data2[predictors])
    return y

if __name__ == "__main__":    
    sql_cmd = "SELECT * FROM %s"%'pankou_data_2017'
    data18 = get_data(sql_cmd)
    del data18['index']   
    data18_Bet365, data18_libo = data_clean(data18)    
    
    predictors_bet365 = ['nor_peilv_win_3','nor_peilv_draw_3','nor_peilv_lose_3','sum_peilvBet365']
    predictors_libo = ['nor_peilv_win_2','nor_peilv_draw_2','nor_peilv_lose_2','sum_peilvlibo']
    predictors_com = ['nor_peilv_win_3','nor_peilv_draw_3','nor_peilv_lose_3','sum_peilvBet365',
    'nor_peilv_win_2','nor_peilv_draw_2','nor_peilv_lose_2','sum_peilvlibo']

    data18_Bet365_train, data18_Bet365_test = cross_validation.train_test_split(data18_Bet365, test_size=0.2, random_state=2) 
    data18_libo_train, data18_libo_test = cross_validation.train_test_split(data18_libo, test_size=0.2, random_state=2) 
    method = SMOTE()
    data18_Bet365_train_new = balanced_data(data18_Bet365_train, predictors_bet365, method)
    data18_libo_train_new = balanced_data(data18_libo_train, predictors_com, method)

    
    '''
    method = SMOTE()
    data18_Bet365_new = balanced_data(data18_Bet365, predictors_bet365, method)
    data18_libo_new = balanced_data(data18_libo, predictors_com, method)
    
    data18_Bet365_train, data18_Bet365_test = cross_validation.train_test_split(data18_Bet365_new, test_size=0.33, random_state=42) 
    data18_libo_train, data18_libo_test = cross_validation.train_test_split(data18_libo_new, test_size=0.33, random_state=42) 
    '''
    '''
    #linear regression
    accuracy = linearRegressionMethod(data18_Bet365_new,predictors_bet365)
    accuracy = linearRegressionMethod(data18_libo,predictors_libo)
    accuracy = linearRegressionMethod(data18_libo,predictors_com)
    '''
    #random forest
    accuracy = RandomForestMethod(data18_Bet365_train_new,predictors_bet365,data18_Bet365_test)
    accuracy = RandomForestMethod(data18_libo_train_new,predictors_libo,data18_libo_test)
    accuracy = RandomForestMethod(data18_libo_train_new,predictors_com,data18_libo_test)
    
    #logistic regression
    accuracy = logisticRegressionMethod(data18_Bet365_train_new,predictors_bet365,data18_Bet365_test)
    accuracy = logisticRegressionMethod(data18_libo_train_new,predictors_libo,data18_libo_test)
    accuracy = logisticRegressionMethod(data18_libo_train_new,predictors_com,data18_libo_test)

    #logistic regression
    accuracy = KNNMethod(data18_Bet365_train_new,predictors_bet365,data18_Bet365_test)
    accuracy = KNNMethod(data18_libo_train_new,predictors_libo,data18_libo_test)
    accuracy = KNNMethod(data18_libo_train_new,predictors_com,data18_libo_test)
    
    #将今日比赛的赔率输入到模型中，进行预测。
    today_matches = standard_todaymatches()
    y = RandomForestPredict(data18_libo_train_new,predictors_com,today_matches)
    today_matches['odd_result'] = 2
    for i in range(len(today_matches)):
        if y[i] == 1:
            today_matches['odd_result'].ix[i] = u'胜'
        if y[i] == 0:
            today_matches['odd_result'].ix[i] = u'平'
        if y[i] == -1:
            today_matches['odd_result'].ix[i] = u'负'
    today_matches.to_csv('C:/Users/Administrator/Desktop/yingchao_season_score/jingcai_today_data_new.csv',encoding='gbk')
    


 