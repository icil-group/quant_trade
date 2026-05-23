import warnings
warnings.filterwarnings("ignore")
import jqdatasdk 
from jqdatasdk import *
import pandas as pd
import os
auth('19371500996','Czs051221') #账号是申请时所填写的手机号；密码为聚宽官网登录密码

pd.set_option('display.max_rows',100000)
pd.set_option('display.max_columns',1000)

#全局变量
data_root = r"C:\Users\czs11\Desktop\python-QT\python_QT_JQ\data/"

def get_stock_list():
    """
    获取所有A股股票列表
    上海证券交易所.XSHG
    深圳证券交易所.XSHE
    :return: stocks_list
    """
    stocks_list = list(jqdatasdk.get_all_securities(["stock"]).index)
    return stocks_list

def get_single_price(code,time_freq,start_date,end_date,fq='none'):
    """
    获取单个股票行情数据
    :param:code
    :param:time_freq
    :start_date
    :end_data
    :fq
    :return: data
    """
    assert fq in ['pre','none','post'],"fq must be pre""none or post"
    data =jqdatasdk.get_price(code, start_date = start_date,end_date = end_date,fq = fq, frequency = time_freq,panel = False) 
    return data

def save_stock_price(data,filename,type):
    """
    保存股票行情数据
    :param data
    :param filename
    :type 股票数据类型可以是:price,finance,valuation   
    """
    assert type in ['finance','price','valuation'],"type must be finance""price or valuation"
    file_root = data_root + type +'/'+ filename +".csv"
    data.index.names = ['date']
    if os.path.exists(file_root): 
        data.to_csv(file_root,mode = 'a',header=False)
        print("已成功追加存储至:",file_root)
    else:
        data.to_csv(file_root,mode = 'w') 
        print("已成功存储至:",file_root)

def get_csv_data(code,type):
    """
    取出股票行情数据
    :param code
    :param type 股票数据类型可以是:price,finace,valuation 
    """
    assert type in ['finance','price','valuation'],"type must be finance""price or valuation"
    file_root = data_root + type +'/'+ code +".csv"
    return pd.read_csv(file_root)

def transfer_price_freq(data,time_freq):
    """
    转换股票行情周期：
    获取周期开盘价（周期第一天的开盘价）,收盘价（周期最后一天的收盘价）,最高价（周期最高价）,最低价（周期最低价）
    :param data
    :param time_freq
    """  
    df_trans = pd.DataFrame()
    df_trans['open']=data.resample(time_freq).first()['open']
    df_trans['close']=data.resample(time_freq).last()['close']
    df_trans['high']=data.resample(time_freq).max()['high']
    df_trans['low']=data.resample(time_freq).min()['low']
    #汇总成交量，成交额
    df_trans['volume']=data.resample(time_freq).sum()['volume']
    df_trans['money']=data.resample(time_freq).sum()['money']
    return df_trans
    
def get_single_finace(code,date,statDate):
    """
    获取单个股票的财务指标
    :param code
    :param date
    :param statDate
    :return: data
    """
    q = query(
        indicator).filter(
        indicator.code == code
    )
    data = jqdatasdk.get_fundamentals(q,date = date, statDate = statDate)
    return data

def get_single_valuation(code,date,statDate):
    """
    获取单个股票的估值指标
    :param code
    :param date
    :param statDate
    :return: data
    """
    q = query(
        valuation).filter(
        valuation.code == code
    )
    data = jqdatasdk.get_fundamentals(q,date = date, statDate = statDate)
    return data

def calculate_change_pct(data):
    """
    涨跌幅的计算: （当期收盘价-上一期收盘价）/当期收盘价
    :param data dataframe,带有收盘价
    :return: dataframe,带有涨跌幅
    """
    data['close_pct'] = (data['close']-data['close'].shift(1))/data['close'].shift(1)
    return data
