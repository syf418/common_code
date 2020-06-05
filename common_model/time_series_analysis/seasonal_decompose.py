# -*- coding: utf-8 -*-
# @Time: 2020/6/4 14:23
import warnings
warnings.filterwarnings(action='ignore')

from matplotlib import pyplot as plt
import statsmodels.api as sm
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

def seasonal_decompose(df, time_col, target_col, freq):
    df.index = df[time_col].values
    res = sm.tsa.seasonal_decompose(df[target_col].values, freq=freq)
    trend = res.trend # 趋势分量
    seasonal = res.seasonal  # 周期分量
    residual = res.resid # 残差分量
    res.plot()
    plt.show()
    return (trend, seasonal, residual)