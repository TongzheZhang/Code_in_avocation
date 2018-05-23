# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 14:39:57 2018
基本功能：给定一组数，若干个赔率，看怎么买是最合适的
线性规划参考网址 https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
一些命名说明：potn-potential, com-combination
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
def cal_com_num(g, least_com, shedan_num):
    total = 0
    for i in range(least_com-shedan_num, g+1-shedan_num):
        total += comb(g-shedan_num, i) 
    return total

# 计算在输入赔率，总场数，最少串联数情况下的所有情况的赔率组合
def cal_odds_list(inputodds, shedan, total_match_num, least_com):
    result = []
    for i,x in enumerate(shedan):
        inputodds.pop(x-i)
    # print inputodds
    for i in range(least_com-shedan_num, total_match_num-shedan_num+1):
        comb = list(combinations(inputodds, i))
        result += comb
    for i in range(len(result)):
        result[i] += tuple(odds_dan)
    return result

# 计算g场比赛，最多错wrong场时，有多少种情况
def cal_situation_num(total_match_num, wrong_match, shedan_num):
    total = 0
    for i in range(0, wrong_match+1):
        total += comb(total_match_num-shedan_num, i) 
    return total

# 在已知总场数，最多预测错场数的情况下，得到所有的可能性，用错场idx表示
def cal_potn_wrong_situation(total_match_num, wrong_match, shedan, all_prob):
    return_list = []
    all_situation_prob = []
    # 所有比赛索引
    idx = list(range(0, total_match_num))
    # 可能错的场次idx
    for x in shedan:
        idx.remove(x)
    '''
    for i, x in enumerate(shedan):
        idx.pop(x-i)
    '''
    # 可能错的场次组合
    for i in range(0, wrong_match+1):
        return_list += list(combinations(idx, i))
    for wrong_match in return_list:
        temp_all_prob = all_prob.copy()
        for i in wrong_match:
            temp_all_prob[i] = 1 - temp_all_prob[i]
        print wrong_match, temp_all_prob, prod(temp_all_prob)
        all_situation_prob.append(prod(temp_all_prob))
    return return_list, all_situation_prob

# 得到所有可能的情况所有赔率组合表
def cal_all_situation_odds_com(odds, all_situation ,shedan, least_com):
    all_odds = []
    tempodds = []
    total_match_num = len(odds)
    for i in range(0, len(all_situation)):
        tempodds = odds[:] # 使用切片，表示复制
        for j in range(len(all_situation[i])):
            tempodds[all_situation[i][j]] = 0
        temp = cal_odds_list(tempodds, shedan, total_match_num, least_com)
        all_odds.append(temp) 
    return all_odds

# 得到所有可能的情况所有赔率值 
def cal_all_situation_odds(all_odds):
    new_all_odds = []
    for i in all_odds:
        temp_odds_list = []
        for j in i:
            temp_odds_list.append(prod(j))
        new_all_odds.append(temp_odds_list)
    return new_all_odds

# 得到所有可能的情况所有期望值,赔率*概率
def cal_all_situation_exp(all_odds_new, all_situation_prob):
    new_all_exp = []
    for idx, row in enumerate(all_odds_new):
        new_all_exp.append(map(lambda x: x*all_situation_prob[idx],row))
    return new_all_exp

# 利用通用概率，计算出组合每种比赛结果的概率
def cal_com_odds(total_match_num, shedan_num, one_prob, wrong_match_num):
    odd = comb(total_match_num-shedan_num, wrong_match_num)*(one_prob**(total_match_num-shedan_num-wrong_match_num))*((1-one_prob)**wrong_match_num)
    return odd

# 计算买彩组合
def cal_all_com(total_match_num, least_com, shedan_num, shedan):
    result = []
    # 所有比赛索引
    idx = list(range(0, total_match_num))
    for x in shedan:
        idx.remove(x)
    for i in range(least_com-shedan_num, total_match_num-shedan_num+1):
        comb = list(combinations(idx, i))
        result += comb
    for i in range(len(result)):
        result[i] += tuple(shedan)
    return result

if __name__ == "__main__":
    
    '''参数设定'''
    # 每场比赛赔率值
    #odds = [1.49, 1.86, 1.61, 1.38, 1.32, 1.16, 3.7, 1.57]
    #odds = [1.50, 1.39, 1.47, 1.63]
    #odds = [1.50, 2, 1.47, 1.63]
    odds = [1.5, 1.5, 1.5, 1.5]
    #odds = [2,3,5]
    # 设胆，第0场到第n-1场，请按数字从小到大输入
    shedan = []
    shedan_num = len(shedan)
    odds_dan = map(lambda i: odds[i], shedan)
    # 总共比赛数
    total_match_num = len(odds)
    # 假设最多预测错几场
    wrong_match_max = 1
    # 最少几场串
    least_com = 2
    least_com = max(least_com, shedan_num)
    # 单场预测对概率，通用概率和实际概率list
    one_prob = 0.85
    all_prob = np.ones(total_match_num)*0.85
    
    '''基本情况输出'''
    print '----------基本情况输出----------'
    print '', all_prob
    if shedan == []:
        print '共%d场比赛，无胆，最少串%d场，最多预测错%d场'%(total_match_num, least_com, wrong_match_max)
    else:
        print '共%d场比赛，第%s场为胆，最少串%d场，假设最多预测错%d场'%(total_match_num, reduce(lambda x, y: str(x)+'&'+str(y), shedan), least_com, wrong_match_max)
    print '共有%d种买彩组合，也就是需要%d个系数'%(cal_com_num(total_match_num, least_com, shedan_num), cal_com_num(total_match_num, least_com, shedan_num))
    print '共有%d种真实比赛结果情况'%(2**total_match_num)
    print '在假设只错%d场及以内假设下（胆对的情况下），共有%d种情况'%(wrong_match_max, cal_situation_num(total_match_num, wrong_match_max, shedan_num))  
    for i in range(0, wrong_match_max+1): 
        print '正确率概率为同一值错%d场比赛的概率是'%i, cal_com_odds(total_match_num, shedan_num, one_prob, i)
    
    print 
    print 
    
    print '哪场比赛预测错误及概率:'
    all_situation, all_situation_prob = cal_potn_wrong_situation(total_match_num, wrong_match_max, shedan, all_prob)
    print 
    print 
    # 得到所有情况的赔率组合
    all_odds = cal_all_situation_odds_com(odds, all_situation, shedan, least_com)
    print '所有情况的赔率组合：', shape(all_odds) #,all_odds
    
    # 得到所有情况的组合赔率值
    all_odds_new = cal_all_situation_odds(all_odds)
    print '所有情况的组合赔率值：', shape(all_odds_new)#, '\n', all_odds_new
    print 
    # 
    all_exp_new = cal_all_situation_exp(all_odds_new, all_situation_prob)
    print all_exp_new
    print 
    
    
    '''线性优化部分'''
    print '----------资金配置部分----------'
    print '我们保证每个只错%d场以内的情况期望为正'%wrong_match_max
    total_money = 1
    total_money_neg = -total_money
    # 目标函数参数
    aim_para = map(sum,zip(*all_exp_new))
    c = map(lambda x: -x, aim_para)
    # 上限参数
    
    A_ub = []
    for i in all_odds_new:
       A_ub.append(map(lambda x:-x, i))
    b_ub = []
    for i in range(0, int(cal_situation_num(total_match_num, wrong_match_max, shedan_num))):
        b_ub.append(total_money_neg) 
        
    # 等式参数  
    A_eq = [np.ones(int(cal_com_num(total_match_num, least_com, shedan_num)))]
    b_eq = [total_money]
    # 权重范围
    bounds = (0, total_money)
    # 线性规划
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, options={"disp":True})
    #print res
    print '----------result----------'
    com = cal_all_com(total_match_num, least_com, shedan_num, shedan)
    for idx, combo in enumerate(com):
        print combo, res['x'][idx]
        
    