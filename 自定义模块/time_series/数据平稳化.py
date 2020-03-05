# -*- coding: utf-8 -*-
# @Time: 2020/3/4 17:42
import warnings
warnings.filterwarnings(action='ignore')

import pandas as pd
import numpy as np
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

def stationary_test(data:DataFrame or Series, window=14):
    '''
    判断数据是稳定的常基于对于时间是常量的几个统计量：
        常量的均值
        常量的方差
        与时间独立的自协方差
    :return:
    '''
    # 计算移动均值和标准差
    rolmean = data.rolling(window).mean()
    rolstd = data.rolling(window).std()

    # plot rolling statistics:
    fig = plt.figure()
    fig.add_subplot()
    orig = plt.plot(data.values, color='blue', label='Original')
    mean = plt.plot(rolmean, color='red', label='rolling mean')
    std = plt.plot(rolstd, color='black', label='Rolling standard deviation')

    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)

    # Dickey-Fuller test:

    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(data, autolag='AIC')
    print(dftest)
    # dftest的输出前一项依次为检测值，p值，滞后数，使用的观测数，各个置信度下的临界值
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical value (%s)' % key] = value

    print(dfoutput)


if __name__ == "__main__":
    df = pd.DataFrame()
    df["time"] = pd.date_range(start="2020-01-01 00:00", periods=40, freq="1min")
    df["y"] = np.random.randn(len(df))

    stationary_test(df["y"], window=7)

