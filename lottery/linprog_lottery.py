# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 14:39:57 2018
基本功能：给定一组数，若干个赔率，看怎么买是最合适的
线性规划参考网址 https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
@author: Richard10ZTZ
"""
from scipy.special import comb, perm
from itertools import combinations
from itertools import product
from scipy.optimize import linprog
from numpy  import *
import numpy as np
# 求积
def prod(L):
    return reduce(lambda x, y: x*y, L)

# 计算出g场比赛共有，多少种彩票组合
def cal_com(g, least_com):
    total = 0
    for i in range(least_com, g+1):
        total += comb(g, i) 
    return total

# 计算在输入概率，总场数，最少串联数情况下的所有情况的概率组合
def cal_odds_list(inputodds, total_match = 8, least_com = 2):
    result = []
    for i in range(least_com, total_match+1):
        result += list(combinations(inputodds, i))
    return result

# 计算g场比赛，最多错wrong场时，有多少种情况
def cal_situation(total_match, wrong_match):
    total = 0
    for i in range(0, wrong_match+1):
        total += comb(total_match, i) 
    return total

# 在已知总场数，最多预测错场数的情况下，得到所有的可能性，用错场idx表示
def get_pro_wrong_com(total_match, wrong_match):
    return_list = []
    for i in range(0, wrong_match+1):
        return_list += list(combinations(idx, i)) 
    return return_list

# 得到所有可能的情况所有赔率组合表
def get_all_odds(odds, all_situation):
    all_odds = []
    tempodds = []
    for i in range(0, len(all_situation)):
        tempodds = odds[:] # 使用切片，表示复制
        for j in range(len(all_situation[i])):
            tempodds[all_situation[i][j]-1] = 0
        all_odds.append(cal_odds_list(tempodds)) 
    return all_odds

# 得到所有可能的情况所有赔率值 
def get_new_odds_list(all_odds):
    new_all_odds = []
    for i in all_odds:
        temp_odds_list = []
        for j in i:
            temp_odds_list.append(prod(j))
        new_all_odds.append(temp_odds_list)
    return new_all_odds

if __name__ == "__main__":
    
    '''参数设定'''
    # 每场比赛赔率值
    #odds = [1.49, 1.86, 1.61, 1.38, 1.32, 1.16, 3.7, 1.57]
    odds = [3, 5, 7]
    # 总共比赛数
    total_match = len(odds)
    # 比赛索引
    idx = list(range(1,total_match+1))
    # 最多预测错几场
    wrong_match = 1
    # 最少几场串
    least_com = 2
    # 单场预测对概率
    one_odd = 0.85
    
    '''基本情况输出'''
    print '共有%d种买彩组合，也就是需要%d个系数'%(cal_com(total_match, least_com), cal_com(total_match, least_com))
    print '共有%d种比赛结果情况'%(2**total_match)
    print '共有%d种情况错了两场以内'%cal_situation(total_match, wrong_match)
    for i in range(0, wrong_match+1):
        odd = comb(total_match, i)*(one_odd**(total_match-i))*((1-one_odd)**i)
        print '错%d场比赛的概率是'%i, odd
    all_situation = get_pro_wrong_com(total_match, wrong_match)
    print '哪场比赛预测错误:',all_situation, len(all_situation)
    
    # 得到所有情况的赔率组合
    all_odds = get_all_odds(odds, all_situation)
    
    #print all_odds
    
    # 得到所有情况的赔率值
    new_all_odds = get_new_odds_list(all_odds)
    
    
    '''线性优化部分'''
    total_money = 1
    neg_total_money = -total_money
    
    # 目标函数参数
    aim_para = map(sum,zip(*new_all_odds))
    c = map(lambda x: -x, aim_para)
    # 上限参数
    A_ub = []
    for i in new_all_odds:
       A_ub.append(map(lambda x:-x, i))
    b_ub = []
    for i in range(0, int(cal_situation(total_match, wrong_match))):
        b_ub.append(neg_total_money)
        
    # 等式参数  
    A_eq = [np.ones(cal_com(total_match, least_com) )]
    b_eq = [total_money]
    # 权重范围
    bounds = (0, total_money)
    # 线性规划
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, options={"disp":True})
    print res
    
    