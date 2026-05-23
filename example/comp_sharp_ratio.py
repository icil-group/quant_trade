#
# Author: czs
# Date: 2026-05-22 22:00:40
# LastEditTime: 2026-05-22 22:25:57
# LastEditors: czs
# Description: 
# FilePath: \python_QT_JQ\example\comp_sharp_ratio.py
#


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
import strategy.base as ba
import matplotlib.pyplot as plt
#获取3只股票数据
data1 =st.get_single_price(code = '000001.XSHE',time_freq = 'daily',start_date = '2025-2-1' ,end_date = '2026-1-31')
data2 =st.get_single_price(code = '000969.XSHE',time_freq = 'daily',start_date = '2025-2-1' ,end_date = '2026-1-31')
data3 =st.get_single_price(code = '002594.XSHE',time_freq = 'daily',start_date = '2025-2-1' ,end_date = '2026-1-31')
#计算每只股票的夏普比率
sharp1 = ba.calculate_sharp(data1)
sharp2 = ba.calculate_sharp(data2)
sharp3 = ba.calculate_sharp(data3)
#可视化3只股票并比较
sharps = {"shap1":sharp1,"sharp2":sharp2,"sharp3":sharp3}
sharps.plot.bar()
#sharp2.plot.bar()
#sharp3.plot.bar()

plt.show()