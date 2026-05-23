"""
用于调用股票行情数据的脚本
"""
import sys
import os
import pandas as pd
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
#初始化变量

if __name__=="__main__":
    code = "000001.XSHE"
    #获取所有股票的数据
    stock_list = st.get_stock_list()
    for stock_code in stock_list:
        data = st.get_single_price(code = stock_code,
                                time_freq = "daily",
                                start_date='2025-02-01',
                                end_date = '2025-03-01')
        st.save_stock_price(data = data,filename = stock_code , type = 'price')
        
 
    #存入csv
    #st.save_stock_price(data = data,filename = stock_code , type = 'price')
    #print(data) 

    #从csv文件中获取数据
    #data = st.get_csv_data(code = "000001.XSHE",type = 'price')
    #print(data)