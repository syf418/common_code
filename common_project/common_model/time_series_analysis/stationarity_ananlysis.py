# -*- coding: utf-8 -*-
# @Time: 2020/3/9 9:49
import warnings
warnings.filterwarnings(action="ignore")

import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa import stattools
import scipy.stats as scs
import statsmodels.api as sm
import statsmodels.tsa.api as smt

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

class stationarity_analysis():
    @staticmethod
    def _show_plot(index, values, title):
        plt.figure(figsize=(10, 6))
        plt.plot(index, values)
        plt.title("{} plot".format(title))
        plt.grid()
        plt.show()

    @staticmethod
    def _ts_plot(data, lags=None, title=''):
        if not isinstance(data, pd.Series):
            data = pd.Series(data)
        with plt.style.context('bmh'):
            plt.figure(figsize=(10, 8))
            layout = (3, 2)
            ts_ax = plt.subplot2grid(layout, (0, 0))
            acf_ax = plt.subplot2grid(layout, (1, 0))
            pacf_ax = plt.subplot2grid(layout, (1, 1))
            qq_ax = plt.subplot2grid(layout, (2, 0))
            pp_ax = plt.subplot2grid(layout, (2, 1))
            data.plot(ax=ts_ax)
            ts_ax.set_title(title + '时序图')
            smt.graphics.plot_acf(data, lags=lags, ax=acf_ax, alpha=0.5)
            acf_ax.set_title('自相关系数')
            smt.graphics.plot_pacf(data, lags=lags, ax=pacf_ax, alpha=0.5)
            pacf_ax.set_title('偏自相关系数')
            sm.qqplot(data, line='s', ax=qq_ax)
            qq_ax.set_title('QQ 图') # 比较的是实际数据分位数跟正态分布时的分位数
            scs.probplot(data, sparams=(data.mean(), data.std()), plot=pp_ax)
            pp_ax.set_title('PP 图') # 比较的时实际数据累积比例和正态分布时的数据累积比例
            plt.tight_layout()
            plt.show()
            return

    def __init__(self, data:DataFrame, target_col:str):
        self.data = data[target_col]
        self.item_name = ''
        self.item = ''

    def acf_pacf(self, nlags, title="", show_plot=True):
        acf = stattools.acf(self.data, nlags=nlags)
        pacf = stattools.pacf(self.data, nlags=nlags)
        self.item_name = "自相关系数(ACF)"
        self.item = acf
        self.__str__()
        self.item_name = "偏自相关系数(PACF)"
        self.item = pacf
        self.__str__()
        if show_plot:
            self._ts_plot(self.data, nlags, title)
        return acf, pacf

    def difference(self, diff=1, show_plot=True):
        """差分平稳化"""
        for i in range(diff):
            self.data = self.data.diff(1)
            if show_plot:
                self._show_plot(self.data.index, self.data.values, "diff {}".format(i+1))
        self.data = self.data.dropna()
        return self.data

    def rolling_statistics(self, window=14, show_plot=True):
        '''
        判断数据是稳定的常基于对于时间是常量的几个统计量：
            常量的均值
            常量的方差
            与时间独立的自协方差
        :return:
        '''
        # 计算移动均值和标准差
        rolmean = self.data.rolling(window).mean()
        rolstd = self.data.rolling(window).std()
        rolcov = self.data.rolling(window).cov()
        rolcorr = self.data.rolling(window).corr()

        if show_plot:
            fig = plt.figure()
            fig.add_subplot()
            plt.plot(self.data.index, self.data.values, color='blue', label='Original')
            plt.plot(rolmean, color='red', label='Rolling mean')
            plt.plot(rolstd, color='black', label='Rolling standard deviation')
            plt.plot(rolcov, color='green', label='Rolling covariation')
            plt.plot(rolcorr, color='purple', label='Rolling correlation coefficient')
            plt.legend(loc='best')
            plt.title('Rolling Values')
            plt.show(block=False)
        return (rolmean, rolstd, rolcov)

    def ADF(self):
        # https://www.jianshu.com/p/aa36f6d01970
        self.data = self.data.dropna()
        dftest = adfuller(self.data.values, autolag='AIC')
        dfoutput = pd.Series(dftest[:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
        for key, value in dftest[4].items():
            dfoutput['Critical value (%s)' % key] = value
        self.item_name = "ADF-Result"
        self.item = dfoutput
        self.__str__()
        return dfoutput, self.data

    def __str__(self):
        print("{} --->\n".format(self.item_name), self.item)

if __name__ == "__main__":
    df = pd.DataFrame()
    df["time"] = pd.date_range(start="2020-01-01 00:00", periods=40, freq="1min")
    df["y"] = np.random.randn(len(df))
    # 实例化
    stationarity_analysis = stationarity_analysis(df, "y")
    # 自相关/偏自相关
    stationarity_analysis.acf_pacf(nlags=10)
    # 差分
    stationarity_analysis.difference(1)
    # 移动窗口统计量
    stationarity_analysis.rolling_statistics(14)
    # 单位根检验
    stationarity_analysis.ADF()
    # 自相关/偏自相关
    stationarity_analysis.acf_pacf(nlags=10)

