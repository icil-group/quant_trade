#
# Author: czs
# Date: 2026-05-22 13:54:48
# LastEditTime: 2026-05-22 21:17:45
# LastEditors: czs
# Description: 
# FilePath: \python_QT_JQ\strategy\strategy.py
#
"""
用来创建交易策略，生成交易信号
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 获取当前文件的绝对路径
current_file = os.path.abspath(__file__)
# 获取当前文件所在目录（example）
current_dir = os.path.dirname(current_file)
# 获取项目根目录
project_root = os.path.dirname(current_dir)

# 将项目根目录添加到Python搜索路径
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import data.stock as st

def compose_signal(data):
    """
    整合信号
    :param data
    :return: data
    """
    #整合多余的信号
    data['buy_signal'] = np.where(((data['buy_signal']==1) & (data['buy_signal'].shift(1)==1)),0,data['buy_signal'])
    data['sell_signal'] = np.where(((data['sell_signal']==-1) & (data['sell_signal'].shift(1)==-1)),0,data['sell_signal'])
    #合并信号
    data['signal'] = data['buy_signal']+ data['sell_signal']
    return data

def calculate_prof_pct(data):
    """
    计算单次开平仓的收益率
    :param data
    :return: data
    """
   
    data.loc[data['signal']!=0,'profit_pct'] = (data['close']-data['close'].shift(1))/data['close'].shift(1)
    data = data[data['signal']==-1]
    return data

def calculate_cum_prof(data):
    """
    计算累计收益率
    :param data
    :return: data
    """
    
    data['cum_prof'] = pd.DataFrame(1+data['profit_pct']).cumprod()-1
    return data

def calculate_max_drawdown(data):
    """
    计算最大回测
    :param data
    :return: data
    """
    #选取时间周期
    window = 252
    #计算周期最大值
    data['roll_max'] = data['close'].rolling(window=252,min_periods=1).max()
    #计算最大值与今天的回测比
    data['daily_dd'] = data['close']/data['roll_max']-1
    #计算出周期内的最大回测比
    data['max_dd'] = data['daily_dd'].rolling(window,min_periods=1).min()
    return data

def calculate_sharp(data):
    """
    计算夏普比率，及其年化夏普比率
    :param data: datafram, stock
    :return sharp,sharp_year
    """
    #公式 sharp = （回报率均值-无风险回报率）/回报率的标准差
    #因子
    daily_return = data['close'].pct_change()
    avg_return = daily_return.mean()
    sd_return = daily_return.std()
    
    #计算夏普比率
    sharp = avg_return /sd_return
    sharp_year = sharp*np.sqrt(252)
    return sharp,sharp_year

def week_period_strategy(code,time_freq,start_date,end_date):
    data = st.get_single_price(code,time_freq,start_date,end_date)

    data['weekday'] = data.index.weekday
    
    #买入信号
    data['buy_signal'] = np.where((data['weekday']==3),1,0)
    #卖出信号
    data['sell_signal'] = np.where((data['weekday']==0),-1,0)   
    data = compose_signal(data)#整合信号
    data = calculate_prof_pct(data)#计算收益率
    data = calculate_cum_prof(data)#计算累计收益率
    data = calculate_max_drawdown(data)#计算最大回撤

    return data


#计算最大回测
# data1 =week_period_strategy(code = '000001.XSHE',time_freq = 'daily',start_date = '2025-2-1' ,end_date = '2026-1-31')
# data2 =week_period_strategy(code = '000969.XSHE',time_freq = 'daily',start_date = '2025-2-1' ,end_date = '2026-1-31')
# data3 =week_period_strategy(code = '002594.XSHE',time_freq = 'daily',start_date = '2025-2-1' ,end_date = '2026-1-31')
# print(data1['max_dd'])
# print(data2['max_dd'])
# print(data3['max_dd'])
# data1['cum_prof'].plot()
# data2['cum_prof'].plot()
# data3['cum_prof'].plot()

#计算夏普比率
data1 =week_period_strategy(code = '000001.XSHE',time_freq = 'daily',start_date = '2025-2-1' ,end_date = '2026-1-31')
df = calculate_sharp(data1)
print(df)
