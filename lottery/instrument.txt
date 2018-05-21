获取数据：
1. Five_League_data: 获取五大联赛近几年数据（主场进球数、客场进球数、主场失球数、客场失球数、主客场比赛次数及主客场赢球次数等）
2. get_JapaneseData: 获取日联杯近几年数据
3. FiveLeagues_recentdata: 获取最近一年的五大联赛的比赛数据，用作测试集，测试预测正确的概率。
4. CupMatches_recentData: 获取杯赛的最近一年比赛数据。（现在仅有日联杯）
5. jingcai_today_data: 获取近几日（可一起投注的）的比赛数据（包括主客场、赔率、bet365初赔、立博初赔）
6. data_pankou: 获取盘口数据（初赔）


7. lottery_expected_return: 用泊松分布的方法，计算胜平负概率，统计用此方法的准确率，并筛选比赛。
8. linprog_lottery: 选取几场比赛，将赔率输入，得到容错一场、并期望最大的资金分配情况。
9. pankouData_classification: 使用两个博彩公司的初赔数据，用不同的机器学习方法，对比赛进行预测。
