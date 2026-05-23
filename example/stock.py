
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
code = '000001.XSHE'
#获取单只股票的数据
data = st.get_single_price(code = code,
                                time_freq = "daily",
                                start_date='2025-02-01',
                                end_date = '2025-03-01')
#计算涨跌幅
print(st.calculate_change_pct(data))

#日k转换成周k
data_week = st.transfer_price_freq(data = data,time_freq="w")

#计算涨跌幅
print(st.calculate_change_pct(data_week))